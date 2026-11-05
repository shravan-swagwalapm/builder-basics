"""Voice settings shootout: same text, several (stability, similarity) variants, fixed seed, mastered.

usage: python3 -I voice_shootout.py OUT_DIR [variants.json]
variants.json = [{"label", "model", "stability", "similarity", "language_code"?, "prefix"?}, ...]
Reads the ElevenLabs key from ~/.config/builder-basics/elevenlabs-key.txt and never prints it.
"""
import json, os, subprocess, sys, urllib.request

VOICE_ID = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "voice.json")))["voice_id"]   # one source of truth: config/voice.json
MODEL = "eleven_v4"
SEED = 42
TEXT = ("Your AI agent can lose your API keys. To one line on a web page... a line nobody can see. "
        "To the model, your prompt and that page? Same thing. Just text. "
        "Save this before your agent gets a browser. Because your agent reads that line. You never will.")
VARIANTS = [  # label, stability, similarity
    ("A_s060_sim075", 0.60, 0.75),
    ("B_s075_sim075", 0.75, 0.75),
    ("C_s060_sim085", 0.60, 0.85),
    ("D_s075_sim085", 0.75, 0.85),
    ("REF_today_s075_sim097", 0.75, 0.97),
]
HERE = os.path.dirname(os.path.abspath(__file__))


def key():
    with open(os.path.expanduser("~/.config/builder-basics/elevenlabs-key.txt")) as f:
        k = "".join(f.read().split())
    if not k.startswith("sk_"):
        sys.exit("key file does not look like an ElevenLabs key")
    return k


def tts(k, v, out):
    payload = {"text": v.get("prefix", "") + TEXT, "model_id": v.get("model", MODEL), "seed": SEED,
               "voice_settings": {"stability": v["stability"], "similarity_boost": v["similarity"]}}
    if v.get("language_code"):
        payload["language_code"] = v["language_code"]
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": k, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"TTS failed for {out}: HTTP {e.code} {e.read()[:300]!r}")
    if len(data) < 10_000:
        sys.exit(f"TTS returned only {len(data)} bytes for {out}")
    open(out, "wb").write(data)


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    k = key()
    variants = (json.load(open(sys.argv[2])) if len(sys.argv) > 2 else
                [{"label": l, "stability": s, "similarity": sim} for l, s, sim in VARIANTS])
    for v in variants:
        label = v["label"]
        raw = os.path.join(out_dir, f"{label}_raw.mp3")
        tts(k, v, raw)
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "master.py"), raw, os.path.join(out_dir, f"{label}.wav")],
                       cwd=out_dir, check=True, capture_output=True)
        print("made", label, flush=True)


if __name__ == "__main__":
    main()
