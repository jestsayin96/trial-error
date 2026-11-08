"""Mirror the whole Poly Haven CC0 library locally. Resumable: re-run any time.

Everything here is CC0 (public domain) - no attribution required.
Only this script belongs in git; the downloads do not.

    python scripts/polyhaven_fetch_all.py          # ~160 GB, 2-4 hours
    TEX_RES=4k python scripts/polyhaven_fetch_all.py

Progress goes to $VILLAGE_ASSETS/fetch_log.txt, state to polyhaven_manifest.json.
Already-downloaded files are skipped, so interrupting it costs nothing.
"""
import os, json, urllib.request, time, sys, traceback

ROOT   = os.environ.get("VILLAGE_ASSETS", os.path.expanduser("~/village_assets"))
LOG    = os.path.join(ROOT, "fetch_log.txt")
MANI   = os.path.join(ROOT, "polyhaven_manifest.json")
UA     = {"User-Agent": "village-fetch"}

TEX_RES   = os.environ.get("TEX_RES",   "2k")
MODEL_RES = os.environ.get("MODEL_RES", "2k")
HDRI_RES  = os.environ.get("HDRI_RES",  "4k")
TEX_MAPS  = ["Diffuse","nor_gl","Rough","AO","Displacement","Metal",
             "arm","Translucent","bump","spec"]

def log(msg):
    line = "%s  %s\n" % (time.strftime("%H:%M:%S"), msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)

def api(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.loads(r.read().decode())
        except Exception:
            if i == tries-1: raise
            time.sleep(2*(i+1))

def fetch(url, path, tries=3):
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".part"
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r:
                data = r.read()
            with open(tmp, "wb") as f:
                f.write(data)
            os.replace(tmp, path)
            return len(data)
        except Exception:
            if os.path.exists(tmp):
                try: os.remove(tmp)
                except Exception: pass
            if i == tries-1: raise
            time.sleep(3*(i+1))

def pick(node, res):
    """best available resolution at or below the requested one"""
    for r in [res, "4k", "2k", "1k", "8k"]:
        if isinstance(node.get(r), dict):
            return node[r]
    return None

def do_texture(aid):
    files = api("https://api.polyhaven.com/files/%s" % aid)
    folder = os.path.join(ROOT, "textures", aid); got = 0; size = 0
    for key in TEX_MAPS:
        node = files.get(key)
        if not isinstance(node, dict): continue
        res = pick(node, TEX_RES)
        if not res: continue
        for fmt in ("jpg","png","exr"):
            e = res.get(fmt)
            if isinstance(e, dict) and e.get("url"):
                size += fetch(e["url"], os.path.join(folder, "%s.%s" % (key, fmt)))
                got += 1
                break
    return got, size

def do_model(aid):
    files = api("https://api.polyhaven.com/files/%s" % aid)
    folder = os.path.join(ROOT, "models", aid); size = 0; got = 0
    res = pick(files.get("blend") or {}, MODEL_RES)
    if not res: return 0, 0
    entry = res.get("blend")
    if not entry: return 0, 0
    size += fetch(entry["url"], os.path.join(folder, "%s.blend" % aid)); got += 1
    for rel, meta in (entry.get("include") or {}).items():
        u = meta.get("url") if isinstance(meta, dict) else None
        if not u: continue
        size += fetch(u, os.path.join(folder, rel.replace("/", os.sep))); got += 1
    return got, size

def do_hdri(aid):
    files = api("https://api.polyhaven.com/files/%s" % aid)
    res = pick(files.get("hdri") or {}, HDRI_RES)
    if not res: return 0, 0
    e = res.get("hdr") or res.get("exr")
    if not e: return 0, 0
    p = os.path.join(ROOT, "hdri", "%s_%s.hdr" % (aid, HDRI_RES))
    return 1, fetch(e["url"], p)

def main():
    open(LOG, "a", encoding="utf-8").close()
    log("=== START  tex=%s model=%s hdri=%s ===" % (TEX_RES, MODEL_RES, HDRI_RES))
    manifest = {}
    if os.path.exists(MANI):
        try: manifest = json.load(open(MANI, encoding="utf-8"))
        except Exception: manifest = {}
    grand = 0
    for kind, fn in [("textures", do_texture), ("hdris", do_hdri), ("models", do_model)]:
        try:
            cat = api("https://api.polyhaven.com/assets?type=%s" % kind)
        except Exception as e:
            log("CATALOG FAIL %s: %s" % (kind, e)); continue
        ids = sorted(cat.keys())
        log("%s: %d assets" % (kind, len(ids)))
        done = manifest.setdefault(kind, {})
        for i, aid in enumerate(ids, 1):
            if done.get(aid, {}).get("ok"):
                continue
            try:
                n, size = fn(aid)
                grand += size
                done[aid] = {"ok": True, "files": n,
                             "name": cat[aid].get("name",""),
                             "tags": cat[aid].get("tags",[])}
                log("[%s %d/%d] %s  %d files  %.1f MB  (total %.2f GB)"
                    % (kind, i, len(ids), aid, n, size/1048576.0, grand/1073741824.0))
            except Exception as e:
                done[aid] = {"ok": False, "err": str(e)[:160]}
                log("[%s %d/%d] %s  FAIL %s" % (kind, i, len(ids), aid, str(e)[:120]))
            if i % 10 == 0:
                json.dump(manifest, open(MANI,"w",encoding="utf-8"), indent=1)
        json.dump(manifest, open(MANI,"w",encoding="utf-8"), indent=1)
    log("=== DONE  %.2f GB this run ===" % (grand/1073741824.0))

if __name__ == "__main__":
    try: main()
    except Exception:
        log("FATAL\n"+traceback.format_exc())
