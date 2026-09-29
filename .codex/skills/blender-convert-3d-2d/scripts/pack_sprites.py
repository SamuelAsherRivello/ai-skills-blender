"""Pack equal-size RGBA PNG frames inside Blender; preserve explicit order and pivot."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy


def pack(manifest_path, output_dir):
    manifest_path, output_dir = Path(manifest_path), Path(output_dir)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    width, height = data["width"], data["height"]
    frames, columns = data["frames"], data.get("columns", 4)
    if not all(isinstance(x, int) and not isinstance(x, bool) and x > 0 for x in (width, height, columns)):
        raise ValueError("Width, height and columns must be positive integers")
    if not 1 <= len(frames) <= 256:
        raise ValueError("Require 1..256 frames")
    columns = min(columns, len(frames))
    rows = math.ceil(len(frames) / columns)
    if width * height * rows * columns > 16777216:
        raise ValueError("Sheet exceeds 16 megapixel bound; split the batch")
    pivot = data.get("pivot", [0.5, 0.5])
    if len(pivot) != 2 or any(not isinstance(x, (int, float)) or not 0 <= x <= 1 for x in pivot):
        raise ValueError("Pivot must have two normalized coordinates")
    if output_dir.exists():
        raise ValueError("Output directory exists; select a fresh run directory")
    loaded, sheet = [], None
    try:
        for frame in frames:
            p = (manifest_path.parent / frame["path"]).resolve()
            if not p.is_file():
                raise ValueError(f"Missing frame: {p.name}")
            img = bpy.data.images.load(str(p), check_existing=False)
            loaded.append(img)
            if tuple(img.size) != (width, height) or img.channels != 4:
                raise ValueError(f"Frame {p.name} must be {width}x{height} RGBA")
        sw, sh = width * columns, height * rows
        pixels = [0.0] * (sw * sh * 4)
        metadata = []
        for index, img in enumerate(loaded):
            x, top = (index % columns)*width, (index // columns)*height
            source = list(img.pixels)
            for y in range(height):
                dst = ((sh - top - height + y)*sw+x)*4
                pixels[dst:dst+width*4] = source[y*width*4:(y+1)*width*4]
            metadata.append({**frames[index], "x": x, "y": top, "width": width, "height": height})
        sheet = bpy.data.images.new("Sprite packing temporary", width=sw, height=sh, alpha=True)
        sheet.pixels.foreach_set(pixels)
        sheet.file_format = 'PNG'
        output_dir.mkdir(parents=True)
        sheet.filepath_raw = str(output_dir / "sheet.png")
        sheet.save()
        result = {"image": "sheet.png", "width": sw, "height": sh, "coordinates": "top-left",
                  "pivot": pivot, "pivot_coordinates": "normalized top-left", "frames": metadata}
        (output_dir / "sheet.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
    finally:
        for img in loaded:
            bpy.data.images.remove(img)
        if sheet is not None:
            bpy.data.images.remove(sheet)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON: width,height,columns,pivot,frames [{path,direction,frame}]")
    parser.add_argument("output_dir", help="New run directory; existing output is never overwritten")
    args = parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    try:
        print(json.dumps(pack(args.manifest, args.output_dir)))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Packing failed: {exc}. Fix input or select a fresh output directory.\n")
