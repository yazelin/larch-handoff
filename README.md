# 交棒總在終點後

《起跑總在開始前》（[larch-start-line](https://github.com/yazelin/larch-start-line)）的下篇，Larch 視覺小說。

整部作品就是一封信：林向晚在女兒程真六歲、快要從幼稚園畢業的時候，替她寫了一封信。信寫到一半，她停下筆抬頭看了一眼，看見的東西決定這封信接下來寫成什麼樣子。三條線各自平行，每條線讀完第一封信，會再接一封很多年以後的信。

形式是 CG 加文字，沒有立繪，沒有地圖。

## 目前進度

- 故事與全部信件文字：完成，經過兩個模型試讀後修過一輪。
- 查證紀錄：完成（`canon/查證紀錄.md`）。
- CG 清單與年紀表：第一版（`canon/CG清單.md`）。
- 視覺小說劇本草稿：由文字自動組成（`canon/劇本草稿.md`）。
- 定錨 19 張、CG 73 張：完成。
- 配樂四首：完成（gemini-web 生成，`assets/audio/`）。音效（口令、槍聲）還沒做。
- Larch：已上架 https://larch.ink/play/market/184feb89-43e1-4a25-a237-8aa468e478f4 （`tools/push.py` 重推）。
- 公開站：https://yazelin.github.io/larch-handoff/ （首頁、原聲帶、查證紀錄，原始檔在 `docs/`）。

## 檔案

| 路徑 | 內容 |
|---|---|
| `canon/設計.md` | 討論過程中定下的每一個決定 |
| `canon/共同段落.md` | 分歧前三條線共用的信 |
| `canon/客廳線.md`、`canon/客廳線-後續.md` | 客廳線第一封與十七歲那封（含學長、學姊兩條） |
| `canon/照片線.md`、`canon/照片線-後續.md` | 照片線第一封與回家前一天那封 |
| `canon/鏡子線.md`、`canon/鏡子線-後續.md` | 鏡子線第一封與收養以後那封 |
| `canon/CG清單.md` | 每一張 CG 對應的文字、畫面、人物年紀 |
| `canon/劇本草稿.md` | 一段一頁的劇本，標出 CG、選項、音樂、音效 |
| `canon/定錨提示詞.md` | 各年紀角色定錨的提示詞 |
| `canon/查證紀錄.md` | 寫稿時查過的事實與來源 |
| `canon/介紹文.md` | 作品介紹文草稿 |
| `assets/art/anchors/` | 角色定錨圖 |
| `assets/art/cg/` | CG |
| `tools/build_script.py` | 從 `canon/` 的文字重新組出劇本草稿 |
| `tools/build_project.py` | 從劇本草稿組出 Larch 專案檔 `project.json` |
| `tools/sheet.py` | 把幾張圖排成一列檢查用 |
| `assets/art/cg/upstream/` | 沿用上篇的 CG（販賣機、終點線後的對望） |
| `tools/cg_jobs.py`、`tools/jobs.py` | 產圖工具與工作定義 |
| `tools/music.py` | 配樂：產生、切循環版、做原聲帶用的完整版 |
| `tools/push.py` | 推上 Larch 私人專案（素材走 jsDelivr 孤兒 tag） |
| `tools/build_site.py` | 公開站的查證紀錄頁；`--tag` 打公開站素材的 tag |
| `assets/audio/` | 配樂：`bgm-*.mp3` 遊戲用循環版、`full/` 原聲帶完整版 |
| `docs/` | 公開站（GitHub Pages） |

## 重新產生劇本草稿與 Larch 專案檔

```bash
python3 tools/build_script.py     # canon/ 的文字 → canon/劇本草稿.md
python3 tools/build_project.py    # 劇本草稿 → project.json（CG 用 assets/art/cg/ 最新的一版）
```

## 本機預覽

```bash
python3 ~/larch-preview/serve.py project.json
```

用 [larch-preview](https://github.com/yazelin/larch-preview) 在本機的 Larch 播放器裡播，按 F 可以在畫面上留回饋。

## 產圖

```bash
CODEX_IMAGE_BASE=<服務網址> CODEX_IMAGE_KEY=<金鑰> python3 tools/cg_jobs.py <工作名>
```

服務網址與金鑰只放在本機，不進 repo。送圖會排隊（`~/.cache/cg_jobs/` 的 `interval`、`max_inflight`）。

## 授權

- 故事文字、劇本、美術、音樂：CC BY-NC 4.0，見 `LICENSE-CONTENT.md`。
- 程式碼（`tools/`）：MIT，見 `LICENSE`。

本作部分內容涉及失去親人與情緒低落。如果你或身邊的人覺得撐不下去，請撥打衛福部安心專線 1925，二十四小時免付費。
