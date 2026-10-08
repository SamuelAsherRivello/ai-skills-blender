[Back to README.md](../README.md)

# Adapt this repository for another skill theme

This repository is a useful layout for a themed skill collection. Copy its structure, then replace its Blender content before publishing under a new name. The generic pieces are the `skills/<name>/SKILL.md` source layout, client package installation, and structural validation. The existing skills, examples, models, references, and safety instructions describe Blender work specifically.

## 1. Define the new catalog

1. Rename or replace each folder in `skills/`. Keep each directory name and its frontmatter `name` identical. Use lowercase letters, numbers, and single hyphens; keep names to 63 characters or fewer.
2. Give each skill a description that says when an agent should use it. Keep the main `SKILL.md` focused on decisions and workflow; put detailed background, fixtures, and longer procedures in nearby `references/` and `scripts/` files linked with relative paths.
3. Remove Blender-only links, commands, tool names, output claims, and assumptions from every copied skill. In particular, `blender-setup` uses Codex-specific diagnostics in the shared source and has a separate Claude adapter; design equivalent setup guidance for the new theme only if it needs one.
4. Update `agents/openai.yaml` when a Codex skill needs display metadata. Claude skills can use the same `SKILL.md` frontmatter without that file.

There is no required number of skills or required ten-step workflow in the generic validator. This Blender catalog can opt into those conventions through validation flags. Do not preserve a numbered workflow just to satisfy a template if a new skill needs a different structure.

## 2. Rebuild client packages

Edit `skills/` for shared behavior. The `.codex/skills/` package has additional Codex-specific skills and operating guidance, so edit it separately when the change applies there. Review `scripts/adapters/claude-blender-setup.md` and the special case in `scripts/sync-client-skills.py`; replace or remove that adapter for a different theme. Regenerate only `.claude/skills/` with:

```sh
python scripts/sync-client-skills.py
```

The PowerShell installers copy the curated Codex or generated Claude package. Their skill-name check is theme-neutral, and they include sibling skills referenced by a selected `SKILL.md`. Review their destination paths and any theme-specific options, especially `-GalleryDestination`, before reusing them. Run `-DryRun` in a temporary project first; installation can replace existing skills only when `-Replace` is explicitly supplied and it makes backups.

## 3. Rewrite repository guidance

- Replace the README title, badge count, screenshots, demo link, skill examples, and client installation examples.
- Update `documentation/getting-started-readme.md`, `documentation/skills-readme.md`, and `CONTRIBUTING.md` for the new catalog.
- Rewrite `AGENTS.md` for the new domain. Its current export, browser inspection, process, and Blender editor rules are specific to this repository; do not silently carry them into unrelated work.
- Review `documentation/examples/`, `documentation/models/`, `documentation/references/`, and `scripts/` individually. The model catalog and viewer export workflow belong to Blender examples. Keep only material that has a real counterpart in the new theme.
- Check the license and attribution before publishing. Do not invent a new copyright holder or reuse contributor claims as template text.

## 4. Validate before release

The validator needs Python 3.9+ and PyYAML (`python -m pip install -r requirements-dev.txt`). On Windows, use `py -3` or a verified Python executable if `python` resolves to a WindowsApps alias. Run the generic structural check on the source and both client packages:

```sh
python scripts/validate-skills.py skills --client codex
python scripts/validate-skills.py .codex/skills --client codex --link-root .codex/skills
python scripts/validate-skills.py .claude/skills --client claude
python scripts/sync-client-skills.py --check
```

The Codex package uses cross-skill links, so `--link-root .codex/skills` allows those package-local targets while rejecting links outside the installed package. The [validation workflow](../.github/workflows/validate-skills.yml) also checks metadata, this Blender catalog's ten-step convention, and generated Claude package drift on pushes and pull requests. Change its optional flags when adapting the catalog. Check a clean installation in each advertised client and invoke at least one skill end to end. Verify any external service or MCP registration separately for each client. Finally, check the README links and compare its skill table with the actual folders.

The `skills` CLI scans both shared and client package directories and currently deduplicates same-name variants. This repository therefore documents direct package installation for Codex and Claude. If the new theme needs client-specific behavior, document which installation route delivers each variant. If every client can use identical source files, a single `skills/` catalog with `npx skills add` may be simpler, as in [mattpocock/skills](https://github.com/mattpocock/skills). Avoid installing both routes into one client because duplicate skill names can make discovery ambiguous.
