# Target package

Use the user's destination. Otherwise use visual-targets/target-01/ for standalone work, or input/visual-targets/target-01/ inside an existing example. Choose the next unused ID for a revision; preserve earlier images and identify the predecessor. Never replace an unrelated file.

| File | Content |
|---|---|
| target.png (or actual image extension) | Inspected generated or supplied image. Absent in prompt-only mode. Copy supplied pixels without modification. |
| prompt.txt | Exact submitted prompt for generation. For supplied images, current interpretation request plus explicit original-prompt status; do not invent the original prompt. |
| brief.md | Observed forms/material/light/composition cues; prioritized 3D actions; prompt conflicts; inferred dimensions/hidden geometry; visible defects and budget limits. |
| manifest.json | Mode, readiness, target identity, image facts, provenance and relative artifact paths. |

Example manifest structure (replace values with evidence):

```json
{
  "target_id": "target-01",
  "mode": "supplied",
  "status": "ready",
  "image": {"path": "target.png", "width": 1536, "height": 1024, "sha256": "actual-file-hash"},
  "prompt": {"path": "prompt.txt", "original_generation_prompt": "unknown"},
  "brief": "brief.md",
  "generation": {"tool": null, "provider": null, "model": null, "seed": null},
  "provenance_note": "User supplied image; original generation metadata not available.",
  "requested_output": {"aspect_ratio": null, "resolution": null},
  "references": [],
  "previous_target_id": null,
  "inspection": {"performed": true, "findings": "Summarize actual inspection; put detail in brief.md."}
}
```

Modes: generated, supplied, prompt-only. Status: ready, needs-revision, missing-image. For prompt-only, set image to null, inspection.performed to false, and status to missing-image. For a supplied file, provenance may include the user's reported origin separately from verified tool metadata. For generated files, record only metadata exposed by the tool, plus the exact prompt and known reference inputs. Null means unknown or unavailable; no seed/model inference from filenames or client branding.

Preserve actual dimensions and file type. A mismatch with requested size/aspect belongs in the inspection findings; if it defeats essential framing, mark needs-revision. An attractive image is not evidence of buildable topology or accurate unseen surfaces.

For delegated work, also record task_id, worker_id when known, and unchanged scene features from the parent brief. Write the final manifest after its referenced artifacts are complete, then notify the parent. Only write inside the assigned target directory.

In the 3D task's comparison record, identify the target ID/hash and genuine Blender render path. Record observed differences, their likely construction/material/lighting causes as hypotheses, corrections made and the follow-up preview result. Target-only requests can deliver criteria without a comparison. Do not claim measured similarity, successful construction or human approval without evidence.
