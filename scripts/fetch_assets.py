"""Download the CC0 PBR texture sets + HDRI this scene depends on.

Run from inside Blender (Scripting tab -> paste -> Run), or:
    blender --background --python scripts/fetch_assets.py

Everything here is CC0 from Poly Haven. Nothing is redistributed in this
repo -- only the IDs and the fetch logic, so the download is reproducible.
"""
import json, os, urllib.request

ROOT = os.environ.get("VILLAGE_ASSETS", os.path.expanduser("~/village_assets"))
TEX  = os.path.join(ROOT, "textures")
HDR  = os.path.join(ROOT, "hdri")
UA   = {"User-Agent": "village-fetch"}
RES  = "2k"
MAPS = ["Diffuse", "nor_gl", "Rough", "Displacement", "AO"]

TEXTURES = [
    "thatch_roof_angled",      # roof
    "medieval_blocks_03",      # stone base, chimney, well
    "white_rough_plaster",     # walls
    "weathered_brown_planks",  # timber framing, door, barrels, crates
    "forest_ground_04",        # grass and dirt path
    "brown_leather",           # training dummy, belts, boots
]
HDRI = "spruit_sunrise"


def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.loads(r.read().decode())


def _fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return os.path.getsize(path)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def grab_texture(asset_id):
    files = _get("https://api.polyhaven.com/files/%s" % asset_id)
    folder = os.path.join(TEX, asset_id)
    os.makedirs(folder, exist_ok=True)
    for key in MAPS:
        node = files.get(key)
        if not isinstance(node, dict):
            continue
        res = node.get(RES) or node.get("1k")
        if not isinstance(res, dict):
            continue
        for fmt in ("jpg", "png", "exr"):
            entry = res.get(fmt)
            if isinstance(entry, dict) and entry.get("url"):
                _fetch(entry["url"], os.path.join(folder, "%s.%s" % (key, fmt)))
                break


def grab_hdri(asset_id):
    os.makedirs(HDR, exist_ok=True)
    files = _get("https://api.polyhaven.com/files/%s" % asset_id)
    url = files["hdri"][RES]["hdr"]["url"]
    _fetch(url, os.path.join(HDR, "%s_%s.hdr" % (asset_id, RES)))


def main():
    os.makedirs(TEX, exist_ok=True)
    for a in TEXTURES:
        print("texture:", a)
        grab_texture(a)
    print("hdri:", HDRI)
    grab_hdri(HDRI)
    total = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, _, fn in os.walk(ROOT) for f in fn
    )
    print("done -> %s (%.1f MB)" % (ROOT, total / 1048576.0))


if __name__ == "__main__":
    main()
