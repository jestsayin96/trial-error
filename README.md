# trial-error

Test bed for an AI-built RPG scene: one house, one adventurer family,
built and rendered in Blender.

## What's here

| Path | What it is |
|---|---|
| `scene/villagetrial.blend` | The scene. Geometry, materials, lights, camera. |
| `renders/` | Rendered stills. |
| `scripts/fetch_assets.py` | Downloads the CC0 textures + HDRI this scene needs. |
| `scripts/polyhaven_fetch_all.py` | Mirrors the **entire** Poly Haven CC0 library locally. |
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

## Mirroring the whole Poly Haven library

`fetch_assets.py` grabs only what this scene uses. To pull everything Poly
Haven publishes — 869 texture sets, 997 HDRIs, 521 models, all CC0 — use:

```bash
python scripts/polyhaven_fetch_all.py
```

Roughly 160 GB and 2-4 hours at 2K textures / 2K models / 4K HDRIs. Override
with `TEX_RES`, `MODEL_RES`, `HDRI_RES`.

It is **resumable**: already-downloaded files are skipped, so interrupting it
costs nothing. Progress is appended to `$VILLAGE_ASSETS/fetch_log.txt` and
state is kept in `polyhaven_manifest.json`.

As with the textures, none of the downloads are committed here — only the
fetch logic, so a fresh clone can rebuild the whole library with one command.
