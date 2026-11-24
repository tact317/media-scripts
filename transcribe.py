import os
import sys
import site
from pathlib import Path

# CUDA / cuDNN のDLL検索パスを保持するためのリスト
# os.add_dll_directory() の戻り値は保持しておく必要があります
_dll_handles = []

# 公式 CUDA Toolkit 12.6 の bin を追加
cuda_bin = r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin"

if Path(cuda_bin).exists():
    _dll_handles.append(os.add_dll_directory(cuda_bin))
    print("DLL追加: CUDA v12.6 bin")
else:
    print(f"CUDAのbinが見つかりません: {cuda_bin}")
    sys.exit(1)

# venv内に pip で入れた cuDNN の bin だけ追加
for sp in site.getsitepackages():
    cudnn_bin = Path(sp) / "nvidia" / "cudnn" / "bin"
    if cudnn_bin.exists():
        _dll_handles.append(os.add_dll_directory(str(cudnn_bin)))
        print("DLL追加:", cudnn_bin)

from faster_whisper import WhisperModel

if len(sys.argv) < 2:
    print("使い方: python transcribe.py 音声ファイル名")
    print("例: python transcribe.py audio_enhanced.mp3")
    sys.exit(1)

audio_path = sys.argv[1]

if not Path(audio_path).exists():
    print(f"ファイルが見つかりません: {audio_path}")
    sys.exit(1)

# GPU使用。RTX 4070ならまず small + float16 で確認
model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16"
)

segments, info = model.transcribe(
    audio_path,
    language="ja",
    task="transcribe",
    vad_filter=True,
    vad_parameters=dict(
        min_silence_duration_ms=900,
        speech_pad_ms=500
    ),
    beam_size=1,
    temperature=0.0,
    condition_on_previous_text=False,
    no_speech_threshold=0.8,
    log_prob_threshold=-0.5,
    compression_ratio_threshold=1.8
)

out_path = Path(audio_path).with_suffix(".txt")

with open(out_path, "w", encoding="utf-8") as f:
    for segment in segments:
        line = f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text.strip()}"
        print(line)
        f.write(line + "\n")

print(f"\n保存しました: {out_path}")