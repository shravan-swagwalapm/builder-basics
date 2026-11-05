"""Generate a voice take from a script using the locked voice config.

usage: python3 -I tts.py VO_TXT OUT_MP3 [--seed N]
VO_TXT: one spoken line per line. Settings come ONLY from ../config/voice.json.
Reads the API key from ~/.config/builder-basics/elevenlabs-key.txt and never prints it.
"""
import json, os, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "..", "config", "voice.json")))


def api_key():
    with open(os.path.expanduser("~/.config/builder-basics/elevenlabs-key.txt")) as f:
        k = "".join(f.read().split())
    if not k.startswith("sk_"):
        sys.exit("key file does not look like an ElevenLabs key")
    return k


def main():
    a = sys.argv[1:]
    src, out = a[0], a[1]
    seed = int(a[a.index("--seed") + 1]) if "--seed" in a else CFG["seed"]
    lines = [l.strip() for l in open(src) if l.strip()]
    text = CFG.get("text_prefix", "") + " ".join(lines)
    payload = {"text": text, "model_id": CFG["model_id"], "seed": seed,
               "voice_settings": {"stability": CFG["stability"], "similarity_boost": CFG["similarity_boost"]}}
    if CFG.get("language_code"):
        payload["language_code"] = CFG["language_code"]
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{CFG['voice_id']}?output_format={CFG['output_format']}",
        data=json.dumps(payload).encode(),
        headers={"xi-api-key": api_key(), "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"TTS failed: HTTP {e.code} {e.read()[:300]!r}")
    if len(data) < 20_000:
        sys.exit(f"TTS returned only {len(data)} bytes")
    open(out, "wb").write(data)
    print(f"wrote {out} ({len(data)//1024} KB, {len(text)} chars, seed {seed})")


if __name__ == "__main__":
    main()
