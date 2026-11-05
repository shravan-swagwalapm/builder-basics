"""Measure motion density, static holds, frame usage, palette for a 9:16 video.
Usage: python3 -I analyze.py <video> ; prints one JSON line."""
import json, subprocess, sys
import numpy as np
from PIL import Image

path = sys.argv[1]
W, H, FPS = 90, 160, 10


def frames(w, h, fps, fmt, ch):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}",
           "-f", "rawvideo", "-pix_fmt", fmt, "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, ch).astype(np.int16)

g = frames(W, H, FPS, "gray", 1)[..., 0]
d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))  # mean abs diff per 0.1s step
moving = d > 1.0
n = len(d)
# longest static hold
best = cur = 0
for m in moving:
    cur = 0 if m else cur + 1
    best = max(best, cur)
# fraction of 1s windows containing motion
win = [moving[i:i + FPS].any() for i in range(0, n - FPS + 1, FPS)]
# motion onsets: static->moving after >=0.3s still
onsets, still = [], 0
for i, m in enumerate(moving):
    if m and still >= 3:
        onsets.append(i / FPS)
    still = 0 if m else still + 1
cuts = int((d > 25).sum())

c = frames(45, 80, 2, "rgb24", 3)
usage, envelope = [], []
for f in c:
    border = np.concatenate([f[0], f[-1], f[:, 0], f[:, -1]])
    q = (border // 16)
    vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[counts.argmax()] * 16 + 8
    content = np.abs(f - bg).max(axis=2) > 40
    usage.append(content.mean())
    rows = np.where(content.mean(axis=1) > 0.03)[0]
    cols = np.where(content.mean(axis=0) > 0.03)[0]
    envelope.append(0 if len(rows) == 0 or len(cols) == 0 else
                    (rows[-1] - rows[0] + 1) * (cols[-1] - cols[0] + 1) / (80 * 45))
mont = Image.fromarray(np.concatenate(list(c.astype(np.uint8)), axis=0))
pal = mont.quantize(colors=6, method=Image.Quantize.MEDIANCUT)
p = pal.getpalette()[:18]
cnt = sorted(pal.getcolors(), reverse=True)
palette = [("#%02X%02X%02X" % tuple(p[i * 3:i * 3 + 3]), round(k / (mont.width * mont.height), 2)) for k, i in cnt]
print(json.dumps({
    "file": path.split("/")[-1], "dur": round(n / FPS, 1),
    "pct_time_moving": round(float(moving.mean()) * 100),
    "pct_1s_windows_with_motion": round(100 * float(np.mean(win))),
    "longest_static_s": best / FPS,
    "motion_onsets": len(onsets),
    "mean_gap_between_onsets_s": round(float(np.mean(np.diff(onsets))) if len(onsets) > 1 else -1, 2),
    "hard_cuts_d25": cuts,
    "frame_usage_pixels_pct": round(100 * float(np.mean(usage))),
    "frame_usage_envelope_pct": round(100 * float(np.mean(envelope))),
    "mean_luma": round(float(g.mean())),
    "palette": palette,
}))
