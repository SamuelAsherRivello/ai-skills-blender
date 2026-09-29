"""Validate standalone skill metadata and linked resources."""
import argparse
from pathlib import Path
import re
import sys
import yaml

CATALOG = ["blender-setup","blender-create-visual-target-2d","blender-create-model","blender-create-environment","blender-procedural-geometry","blender-materials","blender-uv-bake","blender-light-camera","blender-render","blender-rig-animate","blender-game-export","blender-review-optimize","blender-convert-3d-2d","blender-convert-2d-3d"]


def validate(skill, client="codex"):
    skill = Path(skill)
    errors = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return ["missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    try:
        parts = text.split("---", 2)
        if parts[0].strip() or len(parts) != 3:
            raise ValueError("frontmatter delimiters missing")
        meta = yaml.safe_load(parts[1])
        if meta.get("name") != skill.name or not re.fullmatch(r"[a-z0-9-]{1,63}", meta["name"]):
            errors.append("invalid or mismatched name")
        if not isinstance(meta.get("description"), str) or not meta["description"].strip():
            errors.append("missing description")
        if client == "codex":
            ui = yaml.safe_load((skill / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
            if not ui.get("display_name") or not 25 <= len(ui["short_description"]) <= 64:
                errors.append("invalid UI metadata")
            if "$" + skill.name not in ui["default_prompt"]:
                errors.append("default prompt must name skill")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, yaml.YAMLError) as exc:
        errors.append("invalid metadata: " + str(exc))
    steps = re.findall(r"^(\d+)\. ", text, re.M)
    if steps != [str(i) for i in range(1, 11)]:
        errors.append("expected one chronological 1..10 workflow")
    for doc in skill.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if re.match(r"^[a-zA-Z]+://", target) or target.startswith("#"):
                continue
            dest = (doc.parent / target.split("#")[0]).resolve()
            if not dest.is_relative_to(skill.resolve()) or not dest.exists():
                errors.append(f"{doc.name}: missing or nonportable link {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(Path(__file__).resolve().parents[1] / "skills"))
    parser.add_argument("--client", choices=["codex", "claude"], default="codex")
    args = parser.parse_args()
    root = Path(args.path)
    skills = [root] if (root / "SKILL.md").exists() else sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    problems = []
    if root.name == "skills" and {p.name for p in skills} != set(CATALOG):
        problems.append("catalog does not match the fourteen supported skills")
    for skill in skills:
        problems.extend(f"{skill.name}: {e}" for e in validate(skill, args.client))
    print("\n".join(problems) if problems else f"Validated {len(skills)} skills.")
    return bool(problems)


if __name__ == "__main__":
    sys.exit(main())
