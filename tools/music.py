# -*- coding: utf-8 -*-
"""配樂：走 .11 的 gemini-web /api/music，產完切循環、壓到 -16 LUFS（借 ~/larch-taoyuan/bgm.py 的 find_start／make／seam_score）。
服務偶爾逾時，重試就好。網址讀環境變數 GEMINI_WEB_MUSIC_URL，金鑰從 ~/.bashrc 的 GEMINI_IMAGE_KEY 讀，都不進 repo。
  python3 tools/music.py gen [名字…]   → art/music_raw/<名字>.mp3（不進 repo）
  python3 tools/music.py loop [名字…]  → assets/audio/bgm-<名字>.mp3
  python3 tools/music.py full [名字…]  → assets/audio/full/<名字>.mp3（原聲帶用的完整版，-16 LUFS，尾巴淡出）
"""
import base64, importlib.util, json, os, ssl, subprocess, sys, threading, urllib.request
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, OUT = os.path.join(R, 'art/music_raw'), os.path.join(R, 'assets/audio')
URL = os.environ.get('GEMINI_WEB_MUSIC_URL', '')   # 服務網址只從本機環境讀，不進 repo（tools/run_local.sh 會設好）
CTX = ssl._create_unverified_context()   # 內網自簽憑證
CORE = 'soft felt piano carrying a simple tender four-note motif, like a mother writing a letter to her young daughter at a bedroom dresser at night'
# 正常、悲劇、幻想是第二版：第一版樂器沒照指定（Gemini 代聽：悲劇線有弦樂、正常線沒吉他、幻想線沒鋼片琴），改成樂器寫在最前面。
TRACKS = {
    'theme': f'Main theme: {CORE}, warm cello and soft string pads join gently, nostalgic and quietly hopeful, 70 BPM, major key, instrumental, no vocals, loopable',
    'normal': 'Fingerpicked nylon acoustic guitar leads, with soft felt piano and light glockenspiel sparkles, a tender four-note motif, '
               'cozy living room on a weekend evening, father and little daughter laughing, gentle happiness, 78 BPM, major key, instrumental, no vocals, loopable',
    'tragic': 'A single solo felt piano, nothing else: one piano in an empty room, very sparse notes with long silences, soft sustain pedal, '
               'a tender four-note motif played slowly, quiet grief and exhaustion, 58 BPM, minor key, unaccompanied piano solo, instrumental, no vocals, loopable',
    'fantasy': 'Celesta and music box lead a fragile four-note lullaby motif, over floating ambient synth pads and soft harp, dreamlike, shimmering, '
                'a longing for a daughter who exists only in imagination, 64 BPM, instrumental, no vocals, loopable',
}


def key():
    for line in open(os.path.expanduser('~/.bashrc'), encoding='utf-8'):
        if line.startswith('export GEMINI_IMAGE_KEY='): return line.split('=', 1)[1].strip().strip('"')
    raise SystemExit('找不到 GEMINI_IMAGE_KEY')


def one(name, k, tries=4):
    if not URL: raise SystemExit('沒設 GEMINI_WEB_MUSIC_URL')
    os.makedirs(RAW, exist_ok=True)
    for n in range(tries):
        req = urllib.request.Request(URL, method='POST', data=json.dumps({'prompt': TRACKS[name], 'timeout': 720}).encode(),
                                     headers={'Content-Type': 'application/json', 'x-goog-api-key': k})
        try: d = json.load(urllib.request.urlopen(req, timeout=900, context=CTX))
        except Exception as e: print(f'{name} 第{n + 1}次 例外 {e!r}', flush=True); continue
        if d.get('success'):
            open(os.path.join(RAW, f'{name}.mp3'), 'wb').write(base64.b64decode(d['audio']))
            print(f"{name} 好了 {d.get('elapsed_seconds', 0):.0f} 秒", flush=True); return
        print(f"{name} 第{n + 1}次 失敗 {d.get('message') or d.get('error')}", flush=True)
    print(f'{name} 四次都失敗', flush=True)


def loop(name):
    spec = importlib.util.spec_from_file_location('tybgm', os.path.expanduser('~/larch-taoyuan/bgm.py'))
    B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
    src = os.path.join(RAW, f'{name}.mp3'); os.makedirs(OUT, exist_ok=True); out = os.path.join(OUT, f'bgm-{name}.mp3')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    B.LEN = min(90, int(dur) - 4)
    base, best = B.find_start(src), None
    for off in [0, .5, -.5, 1, -1, 1.5, -1.5, 2, -2]:
        s = max(0.0, base + off); B.make(src, s, out); z, d = B.seam_score(out)
        if best is None or abs(z) < abs(best[0]): best = (z, s, d)
        if abs(z) < 3: break
    z, s, d = best; B.make(src, s, out)
    print(f'{name} 原曲 {dur:.0f} 秒 → 循環 {d:.1f} 秒，從 {s:.0f} 秒起，接縫 z={z:+.1f}', flush=True)


def full(name):
    src = os.path.join(RAW, f'{name}.mp3'); out = os.path.join(OUT, 'full', f'{name}.mp3'); os.makedirs(os.path.dirname(out), exist_ok=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-af', f'loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st={dur - 3:.2f}:d=3',
                    '-ar', '44100', '-b:a', '192k', out], check=True)
    print(f'{name} 完整版 {dur:.0f} 秒', flush=True)


if __name__ == '__main__':
    cmd, names = sys.argv[1], sys.argv[2:] or list(TRACKS)
    if cmd == 'gen':
        k = key(); ts = [threading.Thread(target=one, args=(n, k)) for n in names]
        for t in ts: t.start()
        for t in ts: t.join()
    else:
        for n in names: (full if cmd == 'full' else loop)(n)
