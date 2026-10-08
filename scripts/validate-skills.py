"""Validate standalone skill metadata and linked resources."""
import argparse
from pathlib import Path
import re
import sys
import yaml

def validate(skill, client="codex", require_openai_metadata=False, require_ten_steps=False, link_root=None):
    skill = Path(skill)
    allowed_root = Path(link_root).resolve() if link_root else skill.resolve()
    errors = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return ["missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    try:
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        if not match:
            raise ValueError("frontmatter delimiters missing")
        meta = yaml.safe_load(match.group(1))
        if not isinstance(meta, dict):
            raise ValueError("frontmatter must be a mapping")
        name = meta.get("name")
        if name != skill.name or not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 63:
            errors.append("invalid or mismatched name")
        if not isinstance(meta.get("description"), str) or not meta["description"].strip():
            errors.append("missing description")
        ui_path = skill / "agents/openai.yaml"
        if client == "codex" and (require_openai_metadata or ui_path.is_file()):
            ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))["interface"]
            if not ui.get("display_name") or not 25 <= len(ui["short_description"]) <= 64:
                errors.append("invalid UI metadata")
            if "$" + skill.name not in ui["default_prompt"]:
                errors.append("default prompt must name skill")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, yaml.YAMLError) as exc:
        errors.append("invalid metadata: " + str(exc))
    steps = re.findall(r"^(\d+)\. ", text, re.M)
    if require_ten_steps and steps != [str(i) for i in range(1, 11)]:
        errors.append("expected one chronological 1..10 workflow")
    for doc in skill.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            dest = (doc.parent / target.split("#")[0]).resolve()
            if not dest.is_relative_to(allowed_root) or not dest.exists():
                errors.append(f"{doc.name}: missing or nonportable link {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(Path(__file__).resolve().parents[1] / "skills"))
    parser.add_argument("--client", choices=["codex", "claude"], default="codex")
    parser.add_argument("--require-openai-metadata", action="store_true", help="Require agents/openai.yaml for every Codex skill")
    parser.add_argument("--require-ten-step-workflow", action="store_true", help="Enforce this repository's optional 1..10 workflow convention")
    parser.add_argument("--expected-count", type=int, help="Require an exact number of skills")
    parser.add_argument("--link-root", help="Allow existing relative links within this directory (default: each skill)")
    args = parser.parse_args()
    root = Path(args.path)
    if not root.is_dir():
        parser.error(f"skill path is not a directory: {root}")
    skills = [root] if (root / "SKILL.md").exists() else sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    problems = []
    if not skills:
        problems.append("no skill directories found")
    if args.expected_count is not None and len(skills) != args.expected_count:
        problems.append(f"expected {args.expected_count} skills, found {len(skills)}")
    for skill in skills:
        problems.extend(f"{skill.name}: {e}" for e in validate(
            skill, args.client, args.require_openai_metadata, args.require_ten_step_workflow, args.link_root
        ))
    print("\n".join(problems) if problems else f"Validated {len(skills)} skills.")
    return bool(problems)


if __name__ == "__main__":
    sys.exit(main())
