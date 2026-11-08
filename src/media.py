# ============================================================
# src/media.py - Video/âm thanh -> lời thoại (không dùng pydub)
# ============================================================
import os
import shutil
import subprocess
import tempfile
import wave


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def media_ready():
    try:
        import speech_recognition  # noqa: F401
    except ImportError:
        return False, "Thiếu thư viện SpeechRecognition (pip install SpeechRecognition)."
    if not ffmpeg_exe():
        return False, "Không tìm thấy ffmpeg (pip install imageio-ffmpeg hoặc cài ffmpeg)."
    return True, ""


def extract_wav(src_path, wav_path):
    """Tách âm thanh: mono, 16 kHz, PCM 16-bit."""
    cmd = [ffmpeg_exe(), "-y", "-i", src_path, "-vn", "-ac", "1", "-ar", "16000",
           "-acodec", "pcm_s16le", wav_path]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg lỗi: " + r.stderr.decode("utf-8", "ignore")[-300:])


def transcribe_file(src_path, language="vi-VN", chunk_seconds=25, progress=None):
    """Trả về (text, duration_seconds). Cắt đoạn ngắn vì Google Web Speech giới hạn độ dài."""
    import speech_recognition as sr

    rec = sr.Recognizer()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.close()
    try:
        extract_wav(src_path, tmp.name)
        parts = []
        with wave.open(tmp.name, "rb") as w:
            rate, width = w.getframerate(), w.getsampwidth()
            total = w.getnframes()
            duration = total / rate
            step = rate * chunk_seconds
            n_chunks = max(1, -(-total // step))
            for i in range(n_chunks):
                frames = w.readframes(step)
                if not frames:
                    break
                try:
                    parts.append(rec.recognize_google(sr.AudioData(frames, rate, width), language=language))
                except sr.UnknownValueError:
                    pass                      # đoạn im lặng / không nghe được
                except sr.RequestError as e:
                    raise RuntimeError(f"Không gọi được dịch vụ nhận diện giọng nói (cần Internet): {e}")
                if progress:
                    progress((i + 1) / n_chunks)
        return " ".join(parts).strip(), duration
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
