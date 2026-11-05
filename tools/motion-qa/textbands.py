"""Bright text bands in a frame: prints band heights as % of frame height.
Usage: python3 -I textbands.py <video> <t_seconds> <y0_frac> <y1_frac> [lum_threshold]"""
import subprocess, sys
import numpy as np

path, t, y0, y1 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
thr = int(sys.argv[5]) if len(sys.argv) > 5 else 170
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", path, "-frames:v", "1", "-vf", "scale=1080:1920",
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
g = np.frombuffer(raw, np.uint8).reshape(1920, 1080)
a, b = int(y0 * 1920), int(y1 * 1920)
rows = (g[a:b] > thr).sum(axis=1) > 3
bands, start = [], None
for i, r in enumerate(list(rows) + [False]):
    if r and start is None:
        start = i
    if not r and start is not None:
        if i - start >= 4:
            bands.append((a + start, i - start))
        start = None
print(path.split("/")[-1], t, [(round(100 * y / 1920, 1), h, round(100 * h / 1920, 2)) for y, h in bands])
