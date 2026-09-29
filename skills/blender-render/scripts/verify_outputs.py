"""Verify PNG render manifests with Python's standard library; no visual verdict."""
import argparse
import json
from pathlib import Path
import struct
import zlib


def png_info(path):
    raw = Path(path).read_bytes()
    if raw[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f"Not a PNG: {path}")
    pos, header, ended = 8, None, False
    image_data = bytearray()
    while pos < len(raw):
        if pos + 12 > len(raw):
            raise ValueError("Truncated PNG chunk")
        size = struct.unpack(">I", raw[pos:pos+4])[0]
        kind = raw[pos+4:pos+8]
        end = pos + 8 + size
        if end + 4 > len(raw):
            raise ValueError("Truncated PNG data")
        payload = raw[pos+8:end]
        if zlib.crc32(kind + payload) & 0xffffffff != struct.unpack(">I", raw[end:end+4])[0]:
            raise ValueError("PNG checksum mismatch")
        if kind == b'IHDR':
            if header is not None or pos != 8:
                raise ValueError("Invalid PNG header order")
            header = struct.unpack(">IIBBBBB", payload)
        if kind == b'IDAT':
            image_data.extend(payload)
        if kind == b'IEND':
            ended = True
            break
        pos = end + 4
    if not header or not ended or not image_data:
        raise ValueError("Incomplete PNG")
    width, height, depth, color, compression, filtering, interlace = header
    depths = {0: (1,2,4,8,16), 2: (8,16), 3: (1,2,4,8), 4: (8,16), 6: (8,16)}
    if width < 1 or height < 1 or depth not in depths.get(color, ()):
        raise ValueError("Invalid PNG dimensions or pixel format")
    if compression or filtering or interlace:
        raise ValueError("Require standard non-interlaced PNG render output")
    channels = {0:1, 2:3, 3:1, 4:2, 6:4}[color]
    stride = (width * channels * depth + 7) // 8 + 1
    expected = stride * height
    if expected > 256 * 1024 * 1024:
        raise ValueError("PNG exceeds 256 MiB decoded verification limit")
    try:
        decoder = zlib.decompressobj()
        pixels = decoder.decompress(image_data, expected + 1)
    except zlib.error as exc:
        raise ValueError("Invalid PNG compressed pixels") from exc
    if len(pixels) != expected or not decoder.eof or decoder.unused_data:
        raise ValueError("Incomplete or excessive PNG pixel data")
    if any(pixels[row * stride] > 4 for row in range(height)):
        raise ValueError("Invalid PNG scanline filter")
    return {"width": header[0], "height": header[1], "alpha_channel": header[3] in (4, 6)}


def verify(manifest_path):
    path = Path(manifest_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    source = path.parent / data["source"]
    if not source.is_file():
        raise ValueError("Source blend is missing")
    if not data.get("settings") or not data.get("run_id") or not data.get("outputs"):
        raise ValueError("Require run_id, settings and nonempty outputs")
    names, results = set(), []
    for output in data["outputs"]:
        name = output["path"]
        if name in names:
            raise ValueError("Duplicate output path")
        names.add(name)
        info = png_info(path.parent / name)
        for field in ("width", "height"):
            if info[field] != output[field]:
                raise ValueError(f"{name}: incorrect {field}")
        if output.get("alpha") and not info["alpha_channel"]:
            raise ValueError(f"{name}: alpha channel absent")
        results.append({"path": name, **info})
    return {"run_id": data["run_id"], "outputs": results, "visual_quality": "requires image inspection"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON: run_id, source, settings, outputs [{path,width,height,alpha}]")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.manifest), indent=2))
    except (OSError, ValueError, KeyError, TypeError, struct.error) as exc:
        parser.exit(1, f"Verification failed: {exc}. Correct the manifest or rerender affected files.\n")
