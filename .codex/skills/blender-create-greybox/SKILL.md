---
name: blender-create-greybox
description: Quickly communicate a spatial, layout, or silhouette idea in Blender with the fewest clear primitives; use before detailed modeling or as a deliberately low-fidelity deliverable.
---

# blender-create-greybox

## Purpose and scope

Create the least detailed Blender scene that clearly answers the user's question. A greybox communicates scale, occupancy, circulation, layering, sightlines, or a primary silhouette—not a finished asset, realistic architecture, or final art direction.

Use it for requests such as a house massing, city volume study, 2.5D arrangement, level-layout concept, or camera/blocking test. It can also be an early planning step within another Blender task when that reduces uncertainty. Do not treat the greybox as that other skill's final deliverable unless the user asks for a deliberately low-fidelity result.

## Operating boundaries

Read [operating boundaries](../blender-setup/references/operating-boundaries.md) before launching a helper, modifying Blender, capturing editor pixels, or changing an example `.blend`.

## Agent workflow

1. State the spatial question the scene must answer and identify any necessary assumptions about scale, use, and viewing direction before creating content.
2. Create or reuse one dedicated owned collection for the task. Keep generated geometry editable and role-named; use scene-specific role prefixes when several greyboxes share a file. Preserve unrelated scene content and checkpoint before replacing owned geometry.
3. Establish and record a scale convention when scale, clearance, circulation, or contact matters. Treat an inferred convention as an assumption, not a verified fact.
4. Create only the boundary and floor forms needed to establish the spatial frame. Omit either when it cannot clarify the question.
5. Add primary masses, routes, and landmarks in role order using planes, boxes, cylinders, wedges, or other low-sided primitives. Preserve one minimal cue that distinguishes the subject when plain boxes would not: wheels under two masses for a car, a road void among varied-height blocks for a city, or counter/appliance masses inside an open room shell for a kitchen. Add a form only when it makes the requested relationship legible.
6. Validate intended joins, gaps, overlaps, ground contact, and clearances before calling the layout clear. Preserve voids needed for circulation, roads, or an open interior viewing side. Correct only relationships that affect the stated question.
7. Use neutral viewport display by default. Assign a material only when it communicates a required semantic role such as walkable surface, obstacle, boundary, depth layer, or target. When a checker clarifies scale, orientation, or roles, create it procedurally from Object or Generated coordinates with an editable Mapping scale; never use pure black-and-white contrast, image textures, or UV-dependent mapping.
8. Select an intentional proof view: use orthographic views for proportion or alignment questions, and perspective or a minimal role-named camera for spatial experience, silhouette, composition, or fixed sightlines. Frame every critical mass; for an interior, do not let a wall or foreground block conceal the work zone. Inspect actual preview or captured pixels from that view.
9. If inspection reveals ambiguity, make the smallest targeted correction and re-inspect the same proof view. Do not introduce texture maps, UV work, bevels, modifiers, interiors, foliage, props, decals, lighting, or final-art detail unless one directly answers the question.
10. Stop as soon as the answer is visually unambiguous. If refinement is requested, identify the smallest next fidelity step instead of skipping to a finished asset.

## Material language

Use a checker only when it improves the answer to the spatial question. Keep its two cells readable but close in value, with low saturation and a restrained grey hue; it is a scale and grouping cue, not decoration.

For an ordinary scene, choose one named hue family: Slate, Blue, Teal, Sage, Olive, Amber, Terracotta, or Plum. Build every family from the same procedural nodes, mapping controls, checker scale, cell-value contrast, roughness intent, and category hierarchy; hue is the only intended difference. Create all eight only when the user explicitly asks to compare alternatives, and retain the same category map in every version.

Create one shared material datablock for every present semantic category in the owned collection. Name it `Greybox_<Hue>_<Category>` and assign that exact datablock to each object in the category: all floors share `Floor`, all building masses share `Buildings`, and all animal masses share `Animals`. Add categories such as `Route`, `Wall`, or `Landmark` only when they clarify the stated question. Do not split a category because of object identity, repeated placement, footprint, or height; for example, low, mid, and tall buildings normally share `Buildings`.

Report the selected hue, checker scale, present category-to-material map, and every exception to category sharing. If material differentiation would not clarify the question, say that it was intentionally omitted.

## Delivery

Save the editable source when requested. Report the demonstrated question, assumptions, owned collection and key object names, proof view, intentionally omitted detail, and visual-validation status. Make visual-quality claims only from inspected preview or captured pixels; report unavailable validation as unverified.
