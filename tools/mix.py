"""Mix VO + ducked music bed + timed SFX into one track at -14 LUFS / -1 dBTP.

usage: python3 -I mix.py VO_WAV CUES_JSON OUT_WAV
CUES_JSON = {"bed": path, "bed_gain": 0.14, "end": seconds, "sfx": [[path, t_seconds, gain], ...]}
SFX land 1 frame after the picture (+0.033 s), per the motion playbook.
"""
import json, re, subprocess, sys

vo, cues_path, out = sys.argv[1:4]
c = json.load(open(cues_path))
inputs = ["-i", vo, "-i", c["bed"]]
filters = [f"[1:a]atrim=0:{c['end']:.3f},volume={c['bed_gain']},afade=t=in:d=0.8,afade=t=out:st={c['end']-1.2:.3f}:d=1.2[bed]"]
mixins = ["[0:a]", "[bed]"]
for i, (path, t, gain) in enumerate(c["sfx"], start=2):
    inputs += ["-i", path]
    ms = int(round((t + 0.033) * 1000))
    filters.append(f"[{i}:a]volume={gain},adelay={ms}|{ms}[s{i}]")
    mixins.append(f"[s{i}]")
filters.append(f"{''.join(mixins)}amix=inputs={len(mixins)}:normalize=0:duration=first,apad=whole_dur={c['end']:.3f}[pre]")
graph = ";".join(filters)
r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-map", "[pre]",
                    "-ar", "48000", "-ac", "2", "pre_mix.wav"], capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stderr[-1500:])
# two-step loudness: measure, gain to -14, limiter at -1.5 dBFS
def lufs(p):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", e, re.M)[-1]), float(re.findall(r"^\s+Peak:\s+(-?[\d.]+) dBFS", e, re.M)[-1])
g = -14.0 - lufs("pre_mix.wav")[0]
for _ in range(3):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "pre_mix.wav", "-af",
                    f"volume={g:.2f}dB,alimiter=limit=0.84:attack=2:release=50:level=false", out], check=True)
    i, pk = lufs(out)
    if abs(i + 14) <= 0.3:
        break
    g += -14 - i
else:
    sys.exit(f"mix loudness did not converge: {i} LUFS")
subprocess.run(["rm", "-f", "pre_mix.wav"])
print(f"mix: {i} LUFS, peak {pk} dBFS, {len(c['sfx'])} sfx")
