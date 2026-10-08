# Public model delivery

`index.json` is the schema-version-1 catalog consumed by Model Viewer over public HTTP. A model entry represents one `.blend` source path, including historical scenes, with a matching self-contained GLB. Existing game-specific exports remain available separately.

## Regenerate

1. In a disposable Blender 5.2 process with script auto-execution disabled, run `scripts/export_viewer_models.py`. An optional argument after `--` selects one repository-relative `.blend` path. Never run it in a user's open editor: it loads source files and modifies only the in-memory export copy.
2. With Node 24 or later, run `npm ci --prefix scripts/viewer-tools`, then `npm run optimize --prefix scripts/viewer-tools` and `npm run validate --prefix scripts/viewer-tools`. Exports larger than 50 MiB receive lossless meshopt compression, verified by decoded vertex attributes and triangle topology; files above GitHub's 100 MiB limit fail. The validator decodes meshopt first. Inspect each result in the destination viewer: geometry, texture embedding, animation names and duration, scale, transparency, and correspondence with its adjacent render preview.
3. Run `scripts/build_viewer_catalog.py` with Python. It rejects missing exports, stale source hashes, changed GLBs, missing meshes, and external texture/buffer dependencies.
4. Commit the changed `.glb`, `.export.json`, catalog, and associated source changes together. Verify anonymous HTTP access after pushing.

Windows process launches must follow AGENTS.md: explicit no-console creation at every boundary, captured diagnostics, bounded execution, and cleanup. The exporter uses in-process Blender APIs and disables Draco compression; it launches no child helpers. Batch runners must impose a timeout and terminate their owned Blender process on failure. No shell or system console is needed.

An isolated scene built through the existing official MCP may export its selected meshes directly when its source uses packed image textures and needs no procedural bake. Its builder must preserve the editor's previous scene, save an isolated `.blend`, record `exportMethod` and limitations in `.export.json`, and pass the same GLB, hash, catalog, and browser checks. The example-12 greybox house uses this route.

## Contract

- `schemaVersion`: currently `1`.
- `models`: deterministically ordered entries with unique `id` equal to `sourcePath`.
- `title`, `sourcePath`, `glbPath`, `byteSize`, source/export SHA-256 hashes, optional `previewPath`.
- `metadata`: `{label, value, provenancePath}` values extracted from the actual output manifest/review and associated example prompt. Missing information is omitted. AI visual-target manifests are not model statistics.
- `warnings`: documented export limitations. Render previews are references, never substitutes for a working 3D export.
- `exported`: counts/animation names measured from the exported GLB, distinct from Blender scene statistics.
- Optional `view`: source camera position/target in glTF right-handed Y-up coordinates, vertical `frameHeight` at the target and original render `aspect`. This frames the subject even when studio floors are large. Cameras themselves are not exported into the GLB.
- Optional adjacent `catalog.json` may set a source title and `historical: true`; historical entries remain in the catalog after current numbered examples.

All paths are repository-relative and slash-separated. Clients should resolve one source commit per browsing session and load its catalog and assets at that revision. No viewer build or release includes these model bytes.

Procedural base colors and tangent normals are baked into a 2048-pixel atlas per affected scene. Original object/generated texture coordinates are preserved as attributes during static mesh joining; a single shared object-coordinate reference (such as a world-aligned greybox grid Empty) is also preserved for baking. The export retains scene geometry, but Blender world shaders, compositing, and studio lighting are not reproduced. Fine texture detail is resolution-limited; review before publishing. Source `.blend` files are never saved by the exporter.

Eevee Shader-to-RGB toon ramps use their authored lit palette color in a rough PBR material. This preserves the palette but approximates toon lighting. Export reports contain an exporter version and source/GLB hashes; changing exporter behavior requires incrementing its version. Tangents are generated in the browser because Blender emits invalid tangents for some untriangulated source faces. Skinned-mesh non-root validator warnings are expected for the identity armature container used by these exports; browser animation review is required.

Dense procedural surfaces (over 250,000 joined polygons) use per-corner color baking instead of an atlas. This retains the forest's foliage palettes and all geometry. Sub-vertex color variation and procedural bump microdetail are omitted in this case and disclosed in the catalog. The exporter version also changes when this recipe changes.
