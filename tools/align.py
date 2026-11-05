"""Word timings for FINAL (mastered) audio via ElevenLabs forced alignment.

usage: python3 -I align.py AUDIO VO_TXT OUT_JSON
OUT_JSON = {"words": [{"w","s","e","loss"}], "lines": [[start, end], ...one per VO line], "loss": float}
Always run on the mastered file: mastering changes pause lengths, so earlier timestamps would drift.
"""
import json, os, re, sys, uuid, urllib.error, urllib.request


def api_key():
    with open(os.path.expanduser("~/.config/builder-basics/elevenlabs-key.txt")) as f:
        k = "".join(f.read().split())
    if not k.startswith("sk_"):
        sys.exit("key file does not look like an ElevenLabs key")
    return k


def multipart(fields, files):
    b = uuid.uuid4().hex
    out = []
    for k, v in fields.items():
        out += [f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()]
    for k, (name, data, ctype) in files.items():
        out += [f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{name}\"\r\nContent-Type: {ctype}\r\n\r\n".encode(), data, b"\r\n"]
    out.append(f"--{b}--\r\n".encode())
    return b"".join(out), f"multipart/form-data; boundary={b}"


def main():
    audio, vo, out = sys.argv[1:4]
    lines = [l.strip() for l in open(vo) if l.strip()]
    body, ctype = multipart({"text": " ".join(lines)},
                            {"file": (os.path.basename(audio), open(audio, "rb").read(), "audio/wav")})
    req = urllib.request.Request("https://api.elevenlabs.io/v1/forced-alignment", data=body,
                                 headers={"xi-api-key": api_key(), "Content-Type": ctype})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"alignment failed: HTTP {e.code} {e.read()[:300]!r}")
    words = [{"w": w["text"], "s": w["start"], "e": w["end"], "loss": w.get("loss")}
             for w in d["words"] if w["text"].strip()]
    # map words back to VO lines by token count (alignment text == joined lines, so counts match)
    spans, i = [], 0
    for ln in lines:
        n = len(ln.split())
        if i + n > len(words):
            sys.exit(f"alignment returned {len(words)} words, fewer than the script needs at line: {ln!r}")
        spans.append([words[i]["s"], words[i + n - 1]["e"]])
        i += n
    if i != len(words):
        sys.exit(f"word count mismatch: script {i}, aligned {len(words)}")
    json.dump({"words": words, "lines": spans, "loss": d.get("loss")}, open(out, "w"), indent=1)
    print(f"aligned {len(words)} words over {spans[-1][1]:.2f}s, overall loss {d.get('loss')}")


if __name__ == "__main__":
    main()
