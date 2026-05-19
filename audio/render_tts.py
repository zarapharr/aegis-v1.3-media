"""Aegis Academy TTS renderer. ElevenLabs path.

Usage:
  export ELEVENLABS_API_KEY=sk_...
  python3 /tmp/aegis_render_tts.py [voice_id]

Defaults to George voice (executive narration brand match).
"""
import os, sys, json, urllib.request, urllib.error, subprocess
from pathlib import Path

VOICE_ID = sys.argv[1] if len(sys.argv) > 1 else "JBFqnCBsd6RMkjVDRZzb"  # George
MODEL = "eleven_turbo_v2_5"
KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    sys.exit("Set ELEVENLABS_API_KEY first.")

ROOT = Path("/Users/eric_pharr/Projects/Aegis Academy/v1.3/multimedia/audio")
scripts = sorted((ROOT / "scripts").glob("*.txt"))
for s in scripts:
    text = s.read_text()
    body = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.78, "style": 0.25, "use_speaker_boost": True}
    }).encode()
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    req = urllib.request.Request(url, data=body, headers={
        "xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"
    }, method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        audio = resp.read()
    mp3 = ROOT / (s.stem + ".mp3")
    mp3.write_bytes(audio)
    m4a = ROOT / (s.stem + ".m4a")
    subprocess.run(["afconvert", str(mp3), str(m4a), "-d", "aac", "-f", "m4af"], check=True, capture_output=True)
    print(f"  {s.stem}: mp3 {len(audio):,} bytes, m4a {m4a.stat().st_size:,} bytes")
