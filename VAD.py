import sounddevice as sd
import numpy as np
import soundfile as sf
from collections import deque
import time
import os

def record_audio():
    """
    录制音频并保存为 WAV 文件。

    该函数使用声音设备(如麦克风)捕获音频输入,并根据语音活动检测(VAD)算法确定何时开始和结束录音。
    录音将被保存在指定的路径下，每个录音文件对应一段语音活动。
    """
    # 配置录音参数
    sr = 16000  # 采样率
    frame_duration = 0.03  # 每帧的持续时间（秒）
    frame_samples = int(sr * frame_duration)  # 每帧的样本数

    # 语音活动检测（VAD）阈值
    vad_threshold = 0.02  # 能量阈值
    zcr_threshold = 0.3  # 过零率阈值

    # 录音控制参数
    silence_limit = 2.0  # 静音限制（秒），超过该时间无语音活动则结束录音
    min_voice_duration = 0.3  # 最小语音持续时间（秒），避免因短时噪音而开始录音

    # 设置录音文件保存路径
    save_path = "voice"
    os.makedirs(save_path, exist_ok=True)

    # 预缓冲区设置，用于存储可能的语音前置部分
    pre_buffer_duration = 0.5  # 预缓冲区持续时间（秒）
    buffer = deque(maxlen=int(pre_buffer_duration / frame_duration))

    # 录音数据初始化
    recording = []
    recording_active = False
    last_voice_time = time.time()
    voice_duration = 0

    # 控制返回录音路径
    done = False
    filename = None

    def audio_callback(indata, frames, time_info, status):
        """
        音频回调函数，处理实时录音数据。

        参数:
        - indata: 录音数据
        - frames: 帧数
        - time_info: 时间信息（未使用）
        - status: 状态信息（未使用）
        """
        nonlocal recording, recording_active, last_voice_time
        nonlocal voice_duration, done, filename

        audio = indata[:, [0]]
        buffer.append(audio.copy())

        # 计算当前帧的能量和过零率
        energy = np.sqrt(np.mean(audio ** 2))
        zcr = np.mean(np.abs(np.diff(np.sign(audio[:, 0]))))
        now = time.time()

        # 判断当前帧是否为语音
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
