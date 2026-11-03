# -*- coding: utf-8 -*-
"""從 canon/劇本草稿.md 組出 Larch 專案檔 project.json（本機 larch-preview 預覽用，之後也能原樣推上平台）。

一個段落一張對話卡，一頁一句；【CG】標記換背景（寫在那一句的 background，卡片第一句的同時寫在卡片層）；
【選項】變成選擇卡；【轉場】讓下一張卡淡入。CG 用 assets/art/cg/ 底下最新的一版，或 selected.json 指定的那版。
沿用上篇的 CG 放在 assets/art/cg/upstream/。
用法：python3 tools/build_project.py
"""
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cg_jobs import latest

BGM = {"主題曲": "theme", "主題曲・客廳線版（溫暖）": "normal", "主題曲・照片線版（只剩鋼琴）": "tragic", "主題曲・鏡子線版（空靈）": "fantasy"}
UPSTREAM = {"C04": "assets/art/cg/upstream/cg-vending.webp", "F04": "assets/art/cg/upstream/cg-gaze.webp"}


def cg_path(cid):
    if cid in UPSTREAM: return UPSTREAM[cid]
    p = latest("assets/art/cg", cid)
    return os.path.relpath(p, R) if p else None


def parse():
    """回傳段落清單：[{title, lines:[{text, background?}], choice?:[...], transition?}]"""
    secs = []; cur = None; pending_bg = None; pending_tr = False; pending_bgm = None
    for raw in open(os.path.join(R, "canon", "劇本草稿.md")).read().split("\n\n"):
        t = raw.strip()
        if not t or t.startswith("# ") or t == "---" or t.startswith("自動由") or t.startswith("音樂（"): continue
        if t.startswith("## ") or t.startswith("### "):
            cur = {"title": t.lstrip("# ").strip(), "lines": [], "transition": pending_tr}; secs.append(cur); pending_tr = False; continue
        if t.startswith("【CG "):
            pending_bg = cg_path(t[4:-1].strip()); continue
        if t.startswith("【選項】"):
            cur["choice"] = t.split("：", 1)[1].split("／"); cur["prompt"] = t[4:].split("：", 1)[0]; continue
        if t.startswith("【轉場】"): pending_tr = True; continue
        if t.startswith("【BGM】"):
            pending_bgm = f"assets/audio/bgm-{BGM[t[5:].strip()]}.mp3"; continue
        if t.startswith("【"): continue   # 音效還沒做
        line = {"text": t}
        if pending_bg: line["background"] = pending_bg; pending_bg = None
        if pending_bgm: line["bgm"] = pending_bgm; pending_bgm = None
        cur["lines"].append(line)
    return secs


def build():
    secs = parse(); by = {s["title"]: s for s in secs}
    nodes, edges = [], []; x = [0]

    def card(sid, sec, start=False):
        lines = sec["lines"]; bg = next((l["background"] for l in lines if "background" in l), None)
        dl = [{"id": f"l{i}", "speaker": "", "text": l["text"], **({"background": l["background"]} if "background" in l else {}),
               **({"bgm": l["bgm"], "bgmVolume": 0.5, "bgmLoop": True} if "bgm" in l else {})}
              for i, l in enumerate(lines)]
        d = {"type": "dialogue", "title": sec["title"], "speaker": "", "text": dl[0]["text"], "dialogueLines": dl,
             "stage": {"actors": []}, "characterLayers": [], "voiceMode": "off"}
        if bg and "background" in dl[0]: d["background"] = bg
        if "bgm" in dl[0]: d.update(bgm=dl[0]["bgm"], bgmVolume=0.5, bgmLoop=True)
        if start: d.update(transition="fade", transitionMs=1200)   # 後續信前面已經有 interlude 轉場，這裡不再淡入
        if start: d["start"] = True
        nodes.append({"id": sid, "type": "story", "position": {"x": x[0], "y": len(nodes) % 3 * 260}, "data": d}); x[0] += 420
        return sid

    def choice(sid, sec, labels, text="", own_bg=None):
        bg = own_bg or next((l["background"] for l in reversed(sec["lines"]) if "background" in l), None)   # 分歧前那句自己的 CG 優先（C28）
        nodes.append({"id": sid, "type": "story", "position": {"x": x[0], "y": 0}, "data": {
            "type": "choice", "title": sec.get("prompt", "選擇"), "text": text, "background": bg, "choices": labels,
            "choiceMode": "branch", "choicePlacement": "center", "stage": {"actors": []}, "characterLayers": [], "voiceMode": "off"}})
        x[0] += 420; return sid

    def interlude(sid, cg):
        """後續信之前的轉場：全黑停兩秒 → 淡入後續第一張 CG 停兩秒半（作者 2026-11-03：原本只有一次淡入太短）。不用點，自己往下走。"""
        black = {"type": "scene", "title": "轉場：全黑", "text": "", "background": "assets/art/black.webp", "transition": "fadeBlack",
                 "transitionMs": 1800, "autoAdvance": {"enabled": True, "mode": "delay", "delayMs": 2000, "uninterruptible": True},
                 "stage": {"actors": []}, "characterLayers": []}
        show = {"type": "scene", "title": "轉場：CG", "text": "", "background": cg, "transition": "fade",
                "transitionMs": 1500, "autoAdvance": {"enabled": True, "mode": "delay", "delayMs": 2500, "uninterruptible": True},
                "stage": {"actors": []}, "characterLayers": []}
        for k, d in (("-black", black), ("-cg", show)):
            nodes.append({"id": sid + k, "type": "story", "position": {"x": x[0], "y": 520}, "data": d}); x[0] += 420
        return sid + "-black", sid + "-cg"

    def edge(a, b, h="out"):
        edges.append({"id": f"e{len(edges)}", "source": a, "target": b, "sourceHandle": h, "targetHandle": "in"})

    tr = by["共同段落"]; last = tr["lines"].pop()
    t = card("trunk", tr, start=True)
    SAVE_HINT = "\n\n（三條線從這裡分開，建議存檔後再選。）"   # 作者 2026-11-03 要求
    c = choice("pick-look", tr, tr["choice"], last["text"] + SAVE_HINT, last.get("background")); edge(t, c)
    branches = [("normal", "客廳線"), ("tragic", "照片線"), ("fantasy", "鏡子線")]
    for i, (key, name) in enumerate(branches):
        bsec = next(s for s in secs if s["title"].startswith(name + "（"))
        b = card(key, bsec); edge(c, b, f"choice-{i}")
        seq = by[name + "後續"]
        q = seq["lines"].pop() if seq.get("choice") else None
        bk, sh = interlude(key + "-to-seq", next(l["background"] for l in seq["lines"] if "background" in l))
        s1 = card(key + "-seq", seq); edge(b, bk); edge(bk, sh); edge(sh, s1)
        if seq.get("choice"):
            c2 = choice(key + "-pick", seq, seq["choice"], q["text"], q.get("background")); edge(s1, c2)
            end = None
            subs = [s for s in secs if s["title"] in ("學長", "學姊")]
            endsec = by["共同結尾"]
            e = card(key + "-end", endsec)
            for j, sub in enumerate(subs):
                sc = card(f"{key}-sub{j}", sub); edge(c2, sc, f"choice-{j}"); edge(sc, e)
    proj = {"name": "交棒總在終點後", "boards": [{"id": "main", "name": "交棒總在終點後", "nodes": nodes, "edges": edges}]}
    json.dump(proj, open(os.path.join(R, "project.json"), "w"), ensure_ascii=False, indent=1)
    miss = sorted({m for m in re.findall(r"【CG (\w+)】", open(os.path.join(R, "canon", "劇本草稿.md")).read()) if not cg_path(m)})
    print(f"{len(nodes)} 張卡、{len(edges)} 條線；還沒有圖的 CG：{' '.join(miss) or '無'}")


if __name__ == "__main__":
    build()
