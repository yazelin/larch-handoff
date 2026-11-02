# -*- coding: utf-8 -*-
"""《交棒總在終點後》產圖工具（定錨與 CG）。

送圖走跟其他 Larch 作品共用的排隊（~/.cache/cg_jobs/ 的 interval、max_inflight），
服務網址讀環境變數 CODEX_IMAGE_BASE，金鑰讀 CODEX_IMAGE_KEY（都不寫進 repo）。
原圖永遠不覆蓋：每次產出存成 <輸出資料夾>/<名稱>_vN.webp，旁邊放一份同名 .json 記下提示詞與參考圖。
參考圖先縮成長邊 1024 的 JPEG 再送。

用法：python3 tools/cg_jobs.py <工作名> [...]   不帶參數列出全部工作
"""
import base64, io, json, os, sys, threading, time, urllib.request, fcntl, uuid
from PIL import Image

HOME = os.path.expanduser("~")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("CODEX_IMAGE_BASE", "").rstrip("/")
KEY = os.environ.get("CODEX_IMAGE_KEY", "")
QUEUE = os.path.join(HOME, ".cache", "cg_jobs")


def ref(path):
    p = path if os.path.isabs(path) else os.path.join(HOME, path)
    im = Image.open(p)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, (0, 255, 0, 255)); bg.alpha_composite(im); im = bg
    im = im.convert("RGB"); im.thumbnail((1024, 1024))
    b = io.BytesIO(); im.save(b, "JPEG", quality=90); return base64.b64encode(b.getvalue()).decode()


def call(method, path, body=None):
    r = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                               headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as x: return json.loads(x.read())


def _inflight():
    try: live = json.load(open(os.path.join(QUEUE, "inflight.json")))
    except (OSError, ValueError): live = {}
    return {k: t for k, t in live.items() if os.path.exists(f"/proc/{k.split('-')[0]}") and time.time() - t < 1200}


def _queue():
    os.makedirs(QUEUE, exist_ok=True)
    tag = f"{os.getpid()}-{uuid.uuid4().hex}"
    while True:
        with open(os.path.join(QUEUE, "lock"), "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            live = _inflight()
            try: cap = int(open(os.path.join(QUEUE, "max_inflight")).read())
            except (OSError, ValueError): cap = 999
            if len(live) < cap:
                try: gap = float(open(os.path.join(QUEUE, "interval")).read())
                except (OSError, ValueError): gap = 30
                try: last = float(open(os.path.join(QUEUE, "last")).read())
                except (OSError, ValueError): last = 0
                if last + gap > time.time(): time.sleep(last + gap - time.time())
                open(os.path.join(QUEUE, "last"), "w").write(str(time.time()))
                live[tag] = time.time(); json.dump(live, open(os.path.join(QUEUE, "inflight.json"), "w"))
                return tag
        time.sleep(10)


def _done(tag):
    with open(os.path.join(QUEUE, "lock"), "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        live = _inflight(); live.pop(tag, None); json.dump(live, open(os.path.join(QUEUE, "inflight.json"), "w"))


def next_path(outdir, name):
    os.makedirs(outdir, exist_ok=True)
    n = 1
    while os.path.exists(os.path.join(outdir, f"{name}_v{n}.webp")): n += 1
    return os.path.join(outdir, f"{name}_v{n}.webp")


def run(name, j):
    refs = [r() if callable(r) else r for r in j["refs"]]
    body = {"prompt": j["prompt"].strip(), "size": j["size"], "quality": "high", "count": 1,
            "reference_images_base64": [ref(p) for p in refs]}
    tag = _queue()
    try:
        job = call("POST", "/v1/images/jobs", body)["id"]
        t0 = time.time()
        while True:
            time.sleep(15)
            st = call("GET", f"/v1/images/jobs/{job}")
            if st.get("status") == "succeeded":
                data = urllib.request.urlopen(st["images"][0]["url"], timeout=120).read()
                out = next_path(os.path.join(REPO, j["out"]), name)
                Image.open(io.BytesIO(data)).save(out, "WEBP", quality=92)
                json.dump({"job": job, "prompt": body["prompt"], "refs": refs}, open(out[:-5] + ".json", "w"),
                          ensure_ascii=False, indent=1)
                print(f"{name}: OK {int(time.time()-t0)}s -> {out}", flush=True); return out
            if st.get("status") in ("failed", "error"):
                print(f"{name}: FAILED {st.get('error')}", flush=True); return None
    except Exception as e:
        print(f"{name}: ERROR {e}", flush=True); return None
    finally:
        _done(tag)


def latest(outdir, name):
    """某個工作目前最新的一版（給下一階段當參考圖）；選定版可在 <outdir>/selected.json 指定"""
    d = os.path.join(REPO, outdir)
    try:
        sel = json.load(open(os.path.join(d, "selected.json")))
        if name in sel: return os.path.join(d, sel[name])
    except (OSError, ValueError): pass
    vs = sorted([f for f in os.listdir(d) if f.startswith(name + "_v") and f.endswith(".webp")],
                key=lambda f: int(f[len(name) + 2:-5]))
    return os.path.join(d, vs[-1]) if vs else None


if __name__ == "__main__":
    from jobs import JOBS
    names = sys.argv[1:]
    if not names:
        for k in JOBS: print(k)
        sys.exit()
    if not BASE or not KEY:
        sys.exit("CODEX_IMAGE_BASE / CODEX_IMAGE_KEY 沒有設定")
    th = [threading.Thread(target=run, args=(n, JOBS[n])) for n in names]
    for t in th: t.start()
    for t in th: t.join()
