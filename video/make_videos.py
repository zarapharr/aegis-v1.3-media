"""Compose Aegis Academy tier intro videos.

Each video: hero panel held for ~3s + one or two diagram slides + closing brand frame.
Audio: macOS-say TTS that we already produced as .m4a.
Output: H.264 MP4 at 1920x1080, 30fps.
"""
import subprocess
import shutil
from pathlib import Path

MM = Path("/Users/eric_pharr/Projects/Aegis Academy/v1.3/multimedia")
IMG = MM / "images"
DIA = MM / "diagrams"
AUD = MM / "audio"
VID = MM / "video"
TMP = Path("/tmp/aegis_video_work")
TMP.mkdir(exist_ok=True)

# Videos: name → audio file, frame list (each frame: (image_path, duration_sec))
specs = {
    "academy-overview": {
        "audio": AUD / "academy-overview.m4a",
        "frames": [
            (IMG / "academy-overview-hero.png", 6.0),
            (DIA / "01-academy-ladder.png", 8.0),
            (IMG / "aegis-academy-square-logo-mark.png", 3.0),
        ],
    },
    "tier-0-intro": {
        "audio": AUD / "tier-0-intro.m4a",
        "frames": [
            (IMG / "tier-0-hero.png", 6.0),
            (DIA / "01-academy-ladder.png", 8.0),
            (IMG / "tier-0-hero.png", 3.0),
        ],
    },
    "tier-1-intro": {
        "audio": AUD / "tier-1-intro.m4a",
        "frames": [
            (IMG / "tier-1-hero.png", 6.0),
            (DIA / "06-tier1-fit-test.png", 10.0),
            (IMG / "tier-1-hero.png", 3.0),
        ],
    },
    "tier-2-intro": {
        "audio": AUD / "tier-2-intro.m4a",
        "frames": [
            (IMG / "tier-2-hero.png", 6.0),
            (DIA / "02-tier2-delegation-loop.png", 7.0),
            (DIA / "03-tier2-trust-boundary.png", 7.0),
            (DIA / "08-aop-packet-structure.png", 6.0),
            (IMG / "tier-2-hero.png", 3.0),
        ],
    },
    "tier-3-intro": {
        "audio": AUD / "tier-3-intro.m4a",
        "frames": [
            (IMG / "tier-3-hero.png", 6.0),
            (DIA / "04-tier3-pathologies-to-lenses.png", 10.0),
            (DIA / "05-tier3-reversibility-doors.png", 7.0),
            (DIA / "09-decision-review-packet.png", 6.0),
            (IMG / "tier-3-hero.png", 3.0),
        ],
    },
}

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)

def build_video(name, spec):
    audio = spec["audio"]
    frames = spec["frames"]
    # Build concat input file with each frame held for its duration on a 1920x1080 canvas.
    concat_path = TMP / f"{name}.concat.txt"
    # Pad each image to a uniform 1920x1080 frame first.
    padded = []
    for i, (img, dur) in enumerate(frames):
        p_out = TMP / f"{name}-frame-{i:02d}.png"
        # Letterbox-pad to 1920x1080 with cream background.
        cmd = [
            "ffmpeg", "-y", "-i", str(img),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xfdf8ef",
            str(p_out),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        padded.append((p_out, dur))

    with open(concat_path, "w") as f:
        for p, dur in padded:
            f.write(f"file '{p}'\n")
            f.write(f"duration {dur}\n")
        # last file must be repeated without duration per ffmpeg concat-demuxer requirement
        f.write(f"file '{padded[-1][0]}'\n")

    silent_video = TMP / f"{name}.silent.mp4"
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path),
        "-fps_mode", "vfr", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "20",
        "-preset", "medium",
        str(silent_video),
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    final = VID / f"{name}.mp4"
    # Mux video with audio. -shortest stops when shorter ends.
    cmd = [
        "ffmpeg", "-y", "-i", str(silent_video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-map", "0:v:0", "-map", "1:a:0", "-shortest",
        str(final),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    size = final.stat().st_size
    print(f"  {final.name}: {size:,} bytes")

for name, spec in specs.items():
    build_video(name, spec)

print("\nAll 5 videos rendered.")
