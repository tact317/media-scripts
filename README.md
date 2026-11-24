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
