# trial-error

Test bed for an AI-built RPG scene: one house, one adventurer family,
built and rendered in Blender.

## What's here

| Path | What it is |
|---|---|
| `scene/villagetrial.blend` | The scene. Geometry, materials, lights, camera. |
| `renders/` | Rendered stills. |
| `scripts/fetch_assets.py` | Downloads the CC0 textures + HDRI the scene needs. |
| `assets.json` | Which texture sets are used, and for what. |

## Rebuilding from scratch

Textures are **not** committed here — only the IDs and the fetch logic,
so the download stays reproducible without bloating the repo.

```bash
# 1. Pull the CC0 assets (~69 MB from Poly Haven)
python scripts/fetch_assets.py           # or set VILLAGE_ASSETS=/some/path

# 2. Open the scene
blender scene/villagetrial.blend
```

If textures show as missing, point Blender at the asset folder:
**File → External Data → Find Missing Files**.

## The scene

A timber-framed cottage on a stone base with a thatched roof, home to two
working adventurers and their son. Shields flanking the door, crossed
swords and a horned trophy skull on the gable, a guild banner out front, a
weapon rack, a training dummy, supply barrels and crates, lantern posts, a
well.

## Render setup

- **Engine:** Cycles, GPU (HIP), 128 samples, adaptive, denoised
- **Camera:** orthographic, ~69° tilt — fixed isometric-style framing
- **Lighting:** warm key + cool fill + Nishita sky, warm practicals in the windows
- **Grading:** AgX, Medium High Contrast
- **Materials:** box-projected PBR, so no UV unwrapping is needed

## Known gaps

- The figures are built from primitives. Proportions are right, but they
  have no faces, no hands to speak of, and no rig. Real character meshes
  are the next real step up.
- Tree canopies are displaced icospheres, not leaf geometry.
- The banner and shield faces are flat colour, not painted heraldry.
