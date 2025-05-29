import sounddevice as sd
import numpy as np
import soundfile as sf
from collections import deque
import time
import os

def record_audio():
    sr = 16000
    frame_duration = 0.03
    frame_samples = int(sr * frame_duration)

    vad_threshold = 0.02
    zcr_threshold = 0.3

    silence_limit = 2.0
    min_voice_duration = 0.3

    save_path = "voice"
    os.makedirs(save_path, exist_ok=True)

    pre_buffer_duration = 0.5
    buffer = deque(maxlen=int(pre_buffer_duration / frame_duration))

    recording = []
    recording_active = False
    last_voice_time = time.time()
    voice_duration = 0

    # 控制返回录音路径
    done = False
    filename = None

    def audio_callback(indata, frames, time_info, status):
        nonlocal recording, recording_active, last_voice_time
        nonlocal voice_duration, done, filename

        audio = indata[:, [0]]
        buffer.append(audio.copy())

        energy = np.sqrt(np.mean(audio ** 2))
        zcr = np.mean(np.abs(np.diff(np.sign(audio[:, 0]))))
        now = time.time()

        is_voice = (energy > vad_threshold) and (zcr < zcr_threshold)

        if is_voice:
            voice_duration += frames / sr
            last_voice_time = now
            if not recording_active and voice_duration >= min_voice_duration:
                print("开始录音")
                recording.extend([frame.copy() for frame in buffer])
                recording.append(audio.copy())
                recording_active = True

        if recording_active:
            recording.append(audio.copy())

        if recording_active and (now - last_voice_time > silence_limit):
            print(f"结束录音（静音超过 {silence_limit} 秒）")
            filename = f"{save_path}/audio_{int(time.time())}.wav"
            sf.write(filename, np.concatenate(recording), sr)

            recording_active = False
            voice_duration = 0
            buffer.clear()
            recording.clear()
            done = True  # 通知主循环返回路径

    with sd.InputStream(
        channels=1,
        samplerate=sr,
        blocksize=frame_samples,
        callback=audio_callback
    ):
        print("正在监听（每段录音会返回路径）")
        try:
            while True:
                if done and filename:
                    yield filename
                    done = False
                    filename = None
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("已停止监听")
