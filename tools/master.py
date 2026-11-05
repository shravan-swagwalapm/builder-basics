"""Master an ElevenLabs voice take for Shorts: EQ/de-ess/compress, cap pauses, hit -14 LUFS / -1.5 dBFS.

usage: python3 master.py in.mp3 out.wav
"""
import os, re, shutil, subprocess, sys, tempfile

SRC, OUT = sys.argv[1], sys.argv[2]
KEEP = 0.25          # seconds of silence kept per pause
MIN_PAUSE = 0.30     # pauses longer than this get capped to KEEP
THRESH = "-40dB"
TARGET, TOL, MAX_PASSES = -14.0, 0.3, 3
CHAIN = ("highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2,"
         "highshelf=f=10000:g=1.5,deesser=i=0.4,"
         "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120:makeup=2")


def ff(*args):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r.stderr


def duration(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def loudness(p):
    e = ff("-i", p, "-af", "ebur128=peak=true", "-f", "null", "-")
    i = float(re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", e, re.M)[-1])
    pk = float(re.findall(r"^\s+Peak:\s+(-?[\d.]+) dBFS", e, re.M)[-1])
    return i, pk


TMP = tempfile.mkdtemp(prefix="master-")
S1, S2 = os.path.join(TMP, "s1.wav"), os.path.join(TMP, "s2.wav")
ff("-i", SRC, "-af", CHAIN, "-ar", "48000", S1)

# keep speech + KEEP seconds of each long pause (centered), drop the rest
e = ff("-i", S1, "-af", f"silencedetect=noise={THRESH}:d={MIN_PAUSE}", "-f", "null", "-")
starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", e)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
total = duration(S1)
keep, cur = [], 0.0
for s, en in zip(starts, ends):
    s = max(s, 0.0)
    if s == 0.0:                       # leading silence: drop all but 0.05s
        cur = max(en - 0.05, 0.0)
        continue
    mid = (s + en) / 2
    keep.append((cur, mid - KEEP / 2))
    cur = mid + KEEP / 2
keep.append((cur, total))
parts = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[p{i}];" for i, (a, b) in enumerate(keep))
ff("-i", S1, "-filter_complex", parts + "".join(f"[p{i}]" for i in range(len(keep)))
   + f"concat=n={len(keep)}:v=0:a=1[o]", "-map", "[o]", S2)

gain = TARGET - loudness(S2)[0]
for n in range(1, MAX_PASSES + 1):
    ff("-i", S2, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=2:release=50:level=false", OUT)
    i, pk = loudness(OUT)
    print(f"pass {n}: gain {gain:+.2f} dB -> {i} LUFS, peak {pk} dBFS")
    if abs(i - TARGET) <= TOL:
        break
    gain += TARGET - i
else:
    sys.exit(f"loudness did not converge within {MAX_PASSES} passes")

shutil.rmtree(TMP)
print(f"pauses capped: {len(starts)} | duration {duration(SRC):.2f}s -> {duration(OUT):.2f}s")
