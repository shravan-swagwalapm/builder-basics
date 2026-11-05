"""Motion-event timing: duration of contiguous motion runs and where the diff peaks.
peak_frac ~0.1-0.3 => ease-out (fast start, long settle); ~0.5 => in-out.
Usage: python3 -I events.py <video>"""
import json, subprocess, sys
import numpy as np

path = sys.argv[1]
fps = 30
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale=90:160",
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
g = np.frombuffer(raw, np.uint8).reshape(-1, 160, 90).astype(np.int16)
d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
mov = d > 0.8
events, i, n = [], 0, len(d)
while i < n:
    if not mov[i]:
        i += 1
        continue
    j, gap = i, 0
    while j < n and gap <= 1:
        gap = 0 if mov[j] else gap + 1
        j += 1
    seg = d[i:j - gap]
    if 4 <= len(seg) <= 60 and seg.max() < 25:  # 0.13-2s, exclude hard cuts and continuous motion
        events.append((len(seg) / fps, int(seg.argmax()) / len(seg),
                       bool(len(seg) > 6 and seg[-len(seg) // 3:].max() > 0.5 * seg.max())))
    i = j
if events:
    durs = np.array([e[0] for e in events]); pk = np.array([e[1] for e in events])
    print(json.dumps({"file": path.split("/")[-1], "events": len(events),
                      "median_event_s": round(float(np.median(durs)), 2),
                      "p25_p75_s": [round(float(np.percentile(durs, 25)), 2), round(float(np.percentile(durs, 75)), 2)],
                      "median_peak_frac": round(float(np.median(pk)), 2),
                      "pct_peak_in_first_third": round(100 * float((pk < 0.34).mean())),
                      "pct_late_rebound": round(100 * float(np.mean([e[2] for e in events])))}))
