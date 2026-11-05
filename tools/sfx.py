"""Build/refresh the house sound library (ElevenLabs SFX + Music). Cached: existing files are never regenerated.

usage: python3 -I sfx.py OUT_DIR [--music-seconds N]
Reads the API key from ~/.config/builder-basics/elevenlabs-key.txt and never prints it.
"""
import json, os, sys, urllib.error, urllib.request

SFX = {  # name: (prompt, seconds)
    "whoosh-1": ("soft airy UI whoosh, short, clean, modern tech explainer transition", 0.8),
    "whoosh-2": ("subtle fast swoosh, light air movement, minimal", 0.6),
    "pop-1": ("soft rounded UI pop, bubbly, gentle, single", 0.5),
    "pop-2": ("tiny clean interface blip pop, high and soft", 0.5),
    "tick-1": ("very soft keyboard typing ticks, a few keys, quiet", 1.0),
    "click-1": ("single crisp mouse click", 0.5),
    "sweep-1": ("gentle scanning sweep, soft synth shimmer passing left to right", 1.2),
    "impact-1": ("deep soft cinematic impact, warm low thud, not aggressive", 1.0),
    "riser-1": ("short soft tension riser, synth swell, building", 1.6),
    "alert-1": ("subtle low warning tone, two short pulses, calm not alarming", 0.9),
}
MUSIC_PROMPT = ("Calm, modern, minimal electronic instrumental bed for a tech explainer. Soft plucks, warm pads, "
                "light steady pulse around 100 BPM, curious and focused mood, no vocals, no drops, consistent energy, "
                "leaves space for a voiceover.")


def api_key():
    with open(os.path.expanduser("~/.config/builder-basics/elevenlabs-key.txt")) as f:
        k = "".join(f.read().split())
    if not k.startswith("sk_"):
        sys.exit("key file does not look like an ElevenLabs key")
    return k


def post(url, payload, k, out, min_bytes):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"xi-api-key": k, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"{os.path.basename(out)} failed: HTTP {e.code} {e.read()[:300]!r}")
    if len(data) < min_bytes:
        sys.exit(f"{os.path.basename(out)}: only {len(data)} bytes returned")
    open(out, "wb").write(data)


def main():
    a = sys.argv[1:]
    out = a[0]
    music_s = int(a[a.index("--music-seconds") + 1]) if "--music-seconds" in a else 70
    os.makedirs(out, exist_ok=True)
    k = api_key()
    for name, (prompt, secs) in SFX.items():
        f = os.path.join(out, f"{name}.mp3")
        if os.path.exists(f):
            continue
        post("https://api.elevenlabs.io/v1/sound-generation",
             {"text": prompt, "duration_seconds": secs, "prompt_influence": 0.6}, k, f, 2_000)
        print("sfx", name, flush=True)
    f = os.path.join(out, f"bed-calm-{music_s}s.mp3")
    if not os.path.exists(f):
        post("https://api.elevenlabs.io/v1/music",
             {"prompt": MUSIC_PROMPT, "music_length_ms": music_s * 1000, "force_instrumental": True}, k, f, 100_000)
        print("music", os.path.basename(f), flush=True)


if __name__ == "__main__":
    main()
