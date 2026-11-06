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

A half-timbered cottage with a round-tile roof, home to two working
adventurers and their son. Shields hung either side of the arched door, a
guild banner off the eave, spears leaning by the step, a woodpile against
the flank wall, ivy up the front, a hay wagon, crates and fencing.

The house is assembled from the CC0 Quaternius Medieval Village MegaKit on
its 2m module grid. The family are Mixamo characters driven by three
clips (idle / walking / running). Custom pieces — shields, banner, spears,
woodpile, lantern — reuse the kit's own materials so they match.

## Render setup

- **Engine:** Cycles, GPU (HIP), 128 samples, adaptive, denoised
- **Camera:** orthographic, ~69° tilt — fixed isometric-style framing
- **Lighting:** warm key + cool fill + Nishita sky, warm practicals in the windows
- **Grading:** AgX, Medium High Contrast
- **Materials:** box-projected PBR, so no UV unwrapping is needed

## Known gaps

- The characters are semi-realistic Mixamo meshes against a hand-painted
  kit. They don't fully belong. KayKit publishes CC0 rigged adventurers in
  a matching style, but they ship their own rig, so the Mixamo clips
  wouldn't carry over.
- The shield and banner faces are flat colour, not painted heraldry.

## Lighting

Lit at dusk: a low warm sun, a cool blue sky fill, and warm interior light
spilling through the windows from an emissive panel plus point lights
inside the house. A lantern by the door adds a second warm pool. The
contrast between warm practicals and cool shade is what sells it — not the
geometry.
