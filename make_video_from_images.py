from pathlib import Path
import argparse
import subprocess
import tempfile
import re
from datetime import datetime

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}

def parse_time_from_name(path: Path):
    """
    Example:
    スクリーンショット 2026-07-15 210735.png
    """
    s = path.stem
    m = re.search(
        r"(\d{4})-(\d{2})-(\d{2}).*?(\d{2})(\d{2})(\d{2})",
        s
    )
    if m:
        y, mo, d, h, mi, sec = map(int, m.groups())
        return datetime(y, mo, d, h, mi, sec)
    return None

def ffmpeg_path_text(path: Path):
    # ffmpeg concat 用。日本語・空白パス対応のため forward slash にする
    return str(path.resolve()).replace("\\", "/").replace("'", "'\\''")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="画像フォルダ")
    parser.add_argument("-o", "--output", default="output.mp4", help="出力MP4名")
    parser.add_argument("--fps", type=float, default=8, help="画像を進める速度。例: 5, 8, 10")
    parser.add_argument("--video-fps", type=int, default=30, help="出力動画fps")
    parser.add_argument("--hold", type=float, default=1.0, help="最後の画像を止める秒数")
    parser.add_argument("--size", default="1920x1200", help="出力サイズ。例: 1920x1200 / 1920x1080 / original")
    parser.add_argument(
        "--sort",
        choices=["time-in-name", "name", "mtime"],
        default="time-in-name",
        help="並び順"
    )
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    images = [
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ]

    if not images:
        raise RuntimeError("画像が見つかりませんでした。")

    if args.sort == "time-in-name":
        images.sort(key=lambda p: (parse_time_from_name(p) or datetime.min, p.name))
    elif args.sort == "name":
        images.sort(key=lambda p: p.name)
    elif args.sort == "mtime":
        images.sort(key=lambda p: p.stat().st_mtime)

    duration = 1.0 / args.fps

    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", delete=False, encoding="utf-8"
    ) as f:
        list_path = Path(f.name)

        for p in images[:-1]:
            f.write(f"file '{ffmpeg_path_text(p)}'\n")
            f.write(f"duration {duration}\n")

        # 最後の画像は少し長めに止める
        last = images[-1]
        f.write(f"file '{ffmpeg_path_text(last)}'\n")
        f.write(f"duration {duration + args.hold}\n")
        f.write(f"file '{ffmpeg_path_text(last)}'\n")

    if args.size.lower() == "original":
        vf = f"fps={args.video_fps},format=yuv420p"
    else:
        width, height = args.size.lower().split("x")
        vf = (
            f"fps={args.video_fps},"
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
            f"format=yuv420p"
        )

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_path),
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        args.output,
    ]

    print("画像枚数:", len(images))
    print("先頭:", images[0].name)
    print("最後:", images[-1].name)
    print("出力:", args.output)
    print("実行中...")

    subprocess.run(cmd, check=True)

    print("完了:", args.output)

if __name__ == "__main__":
    main()