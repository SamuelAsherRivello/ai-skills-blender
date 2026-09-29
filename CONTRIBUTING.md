# Contributing

Contributions are welcome! Whether you are new to Blender, trying AI-assisted workflows, or improving an existing skill, there is room to help. Small fixes, questions, and suggestions are welcome too.

## Ways to contribute

- Report bugs or confusing instructions.
- Suggest new skills or improvements to existing workflows.
- Improve documentation, prompts, and examples.
- Share reproducible results from different Blender versions, AI clients, or operating systems.
- Fix helper scripts or improve validation.

## Issues and ideas

Check the [existing issues](https://github.com/SamuelAsherRivello/ai-skills-blender/issues) for related discussions, or [open an issue](https://github.com/SamuelAsherRivello/ai-skills-blender/issues/new) to start one. For larger changes, an issue is a useful place to discuss the approach first.

For bug reports, include what you tried, what you expected, what happened, and steps to reproduce it. Mention your operating system, AI client, and Blender version when relevant. Include useful error messages or images, with credentials and personal information removed.

## Pull requests

1. Fork the repository and create a branch for your change.
2. Read the [getting started guide](documentation/getting-started-readme.md) and [repository instructions](AGENTS.md).
3. Make a focused change. Author shared skills in [skills/](skills/); the Claude setup adapter lives in [scripts/adapters/](scripts/adapters/). Regenerate client copies with [sync-client-skills.py](scripts/sync-client-skills.py) when those sources change.
4. Check the affected behavior and links. See the [helper and validation guide](scripts/script-documentation/helpers.md) for available checks. Describe what you tested and anything you could not verify.
5. [Open a pull request](https://github.com/SamuelAsherRivello/ai-skills-blender/pulls) explaining the problem, your changes, and any related issue. Draft pull requests are welcome for work in progress.

Keep discussions respectful and constructive. Ask questions if you are unsure where to start—we welcome collaboration at every experience level.
