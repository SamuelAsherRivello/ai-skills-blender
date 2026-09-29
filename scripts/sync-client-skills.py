"""Generate checked-in client packages from shared skill sources; --check detects drift."""
import argparse
from pathlib import Path
import sys


def expected_files(repo, client):
    files = {}
    for source in (repo / "skills").rglob("*"):
        if not source.is_file() or "__pycache__" in source.parts or source.suffix in (".pyc", ".pyo"):
            continue
        relative = source.relative_to(repo / "skills")
        if client == "claude":
            if "agents" in relative.parts:
                continue
            if relative.parts[0] == "blender-setup":
                if str(relative).replace("\\", "/") != "blender-setup/SKILL.md":
                    continue
                files[relative] = (repo / "scripts/adapters/claude-blender-setup.md").read_bytes()
                continue
        files[relative] = source.read_bytes()
    return files


def sync(repo, check=False):
    errors = []
    for client in ("codex", "claude"):
        target = repo / ("." + client) / "skills"
        expected = expected_files(repo, client)
        existing = {p.relative_to(target) for p in target.rglob("*") if p.is_file()
                    and "__pycache__" not in p.parts and p.suffix not in (".pyc", ".pyo")}
        extra = existing - set(expected)
        if extra:
            errors.append(f"{client}: unexpected package files: {sorted(map(str, extra))}; review manually")
        for relative, data in expected.items():
            path = target / relative
            if not path.exists() or path.read_bytes() != data:
                if check:
                    errors.append(f"{client}: stale or missing {relative}")
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = sync(Path(__file__).resolve().parents[1], args.check)
    print("\n".join(errors) if errors else "Codex and Claude skill packages are synchronized.")
    sys.exit(bool(errors))
