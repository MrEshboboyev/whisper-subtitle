import sys
import os
from faster_whisper import WhisperModel


VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}


def format_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_time(seg.start)
            end = format_time(seg.end)

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{seg.text.strip()}\n\n")


def is_video(file):
    return os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS


def process_video(model, video_path):
    print(f"\n🎬 Processing: {video_path}")

    output_path = os.path.splitext(video_path)[0] + ".srt"

    segments, info = model.transcribe(
        video_path,
        language="en"
    )

    write_srt(segments, output_path)

    print(f"✅ Saved: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <file_or_folder>")
        sys.exit(1)

    path = sys.argv[1]

    model = WhisperModel(
        "small",
        device="cuda",
        compute_type="float16"
    )

    if os.path.isfile(path):
        process_video(model, path)

    elif os.path.isdir(path):
        files = sorted(os.listdir(path))

        videos = [
            os.path.join(path, f)
            for f in files
            if is_video(f)
        ]

        if not videos:
            print("No video files found.")
            return

        print(f"📁 Found {len(videos)} videos")

        for v in videos:
            process_video(model, v)

    else:
        print("Invalid path")


if __name__ == "__main__":
    main()
