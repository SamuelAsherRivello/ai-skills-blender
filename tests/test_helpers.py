import importlib.util
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


validator = load("scripts/validate-skills.py", "validator")
render = load("skills/blender-render/scripts/verify_outputs.py", "render")


def png(width=2, height=3, alpha=True):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind+data) & 0xffffffff)
    channels = 4 if alpha else 3
    raw = b"".join(b"\0" + b"\xff" * (width*channels) for _ in range(height))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width,height,8,6 if alpha else 2,0,0,0)) + chunk(b"IDAT",zlib.compress(raw)) + chunk(b"IEND",b"")


class HelperTests(unittest.TestCase):
    def test_valid_and_broken_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "blender-render"
            shutil.copytree(ROOT/"skills/blender-render",folder)
            self.assertEqual(validator.validate(folder), [])
            (folder/"scripts/verify_outputs.py").unlink()
            self.assertTrue(any("missing" in e for e in validator.validate(folder)))
            (folder/"agents/openai.yaml").unlink()
            self.assertTrue(any("metadata" in e for e in validator.validate(folder)))

    def test_invalid_name(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)/"BAD_NAME"
            shutil.copytree(ROOT/"skills/blender-render",folder)
            self.assertTrue(any("name" in e for e in validator.validate(folder)))

    def test_png_and_manifest_failures(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"source.blend").write_bytes(b"test fixture")
            (root/"a.png").write_bytes(png())
            manifest={"run_id":"test","source":"source.blend","settings":{"engine":"test"},
                      "outputs":[{"path":"a.png","width":2,"height":3,"alpha":True}]}
            path=root/"manifest.json"
            path.write_text(json.dumps(manifest))
            self.assertEqual(len(render.verify(path)["outputs"]),1)
            manifest["outputs"][0]["width"]=5
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,"width"): render.verify(path)
            manifest["outputs"][0]["width"]=2
            path.write_text(json.dumps(manifest))
            (root/"a.png").write_bytes(png(alpha=False))
            with self.assertRaisesRegex(ValueError,"alpha"): render.verify(path)
            (root/"a.png").write_bytes(png()[:-4])
            with self.assertRaises(ValueError): render.verify(path)
            (root/"a.png").unlink()
            with self.assertRaises(OSError): render.verify(path)

    def test_png_requires_decodable_pixels(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"bad.png"
            valid=png()
            # IHDR followed directly by IEND has valid chunk checksums but no pixels.
            path.write_bytes(valid[:33]+valid[-12:])
            with self.assertRaisesRegex(ValueError,"Incomplete"): render.png_info(path)
            payload=b"not-zlib"
            chunk=struct.pack(">I",len(payload))+b"IDAT"+payload+struct.pack(">I",zlib.crc32(b"IDAT"+payload)&0xffffffff)
            path.write_bytes(valid[:33]+chunk+valid[-12:])
            with self.assertRaisesRegex(ValueError,"compressed"): render.png_info(path)


if __name__ == "__main__":
    unittest.main()
