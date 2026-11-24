# media-scripts

Small personal utilities.

| Script | What it does | Needs |
|---|---|---|
| `transcribe.py` | Transcribes a Japanese audio file with faster-whisper (large-v3, GPU, VAD on) and writes `<audio>.txt` with timestamps | Python, `faster-whisper`, CUDA 12.6 + cuDNN |
| `make_video_from_images.py` | Turns a folder of screenshots into a video, ordered by the timestamp in each file name | Python, ffmpeg on PATH |

```
python transcribe.py audio.mp3
python make_video_from_images.py --help
```

## autohotkey/

- `taskbartoggle.ahk`（AutoHotkey **v1** 構文）：Ctrl+Shift+A でタスクバーの表示・非表示を切り替えます（マルチモニター対応）。Ctrl+Shift+Esc で終了します。
- `notion.ahk`（AutoHotkey **v2**）：Notion の Ctrl+Shift+K を無効にします。元は対象がインストーラ（`Notion Setup 4.12.1.exe`）になっていたので、`Notion.exe` に直しました。
