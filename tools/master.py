"""Master an ElevenLabs voice take for Shorts: slow to config tempo, EQ/de-ess/compress,
set every sentence pause to config pause_s, hit -14 LUFS / -1.5 dBFS.

usage: python3 master.py in.mp3 out.wav
"""
import json, os, re, shutil, subprocess, sys, tempfile

SRC, OUT = sys.argv[1], sys.argv[2]
_CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "voice.json")))
TEMPO = _CFG["tempo"]      # eleven_v4 ignores voice_settings.speed (A/B 2026-11-06: same length), so pace is set here
KEEP = _CFG["pause_s"]     # every pause >= MIN_PAUSE becomes exactly KEEP seconds (shortened or lengthened)
MIN_PAUSE = 0.30           # shorter gaps (commas, breaths) are left as spoken
THRESH = "-40dB"
TARGET, TOL, MAX_PASSES = -14.0, 0.3, 3
CHAIN = (f"atempo={TEMPO},"
         "highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1.0:g=2,"
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

# every long pause becomes exactly KEEP seconds: trim around its middle, or pad silence into its middle.
# (Before 2026-11-06 this loop REMOVED KEEP from each pause instead of keeping KEEP: 21 pauses x 0.25 s = the
#  5.25 s lost on the Kimi take, turning 0.35 s sentence breaks into 0.10 s — "feels fast".)
e = ff("-i", S1, "-af", f"silencedetect=noise={THRESH}:d={MIN_PAUSE}", "-f", "null", "-")
starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", e)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
total = duration(S1)
segs, cur = [], 0.0                    # ("a", start, end) = audio slice; ("z", dur) = inserted silence
for s, en in zip(starts, ends):
    s = max(s, 0.0)
    if s == 0.0:                       # leading silence: drop all but 0.05s
        cur = max(en - 0.05, 0.0)
        continue
    mid = (s + en) / 2
    if en - s >= KEEP:
        segs.append(("a", cur, mid - KEEP / 2))
        cur = mid + KEEP / 2
    else:
        segs += [("a", cur, mid), ("z", KEEP - (en - s))]
        cur = mid
segs.append(("a", cur, total))
parts = "".join(f"[0:a]atrim={g[1]:.3f}:{g[2]:.3f},asetpts=PTS-STARTPTS[p{i}];" if g[0] == "a"
                else f"aevalsrc=0:d={g[1]:.3f}:s=48000:c=mono,asetpts=PTS-STARTPTS[p{i}];"
                for i, g in enumerate(segs))
ff("-i", S1, "-filter_complex", parts + "".join(f"[p{i}]" for i in range(len(segs)))
   + f"concat=n={len(segs)}:v=0:a=1[o]", "-map", "[o]", S2)

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
print(f"tempo {TEMPO} | pauses set to {KEEP}s: {len(starts)} | duration {duration(SRC):.2f}s -> {duration(OUT):.2f}s")
