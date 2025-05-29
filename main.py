import threading
import queue
import time
import multiprocessing

from VAD import record_audio  # 每次自动录一段
from ASR import transcribe
from LLM import get_intent
from control import control_device
from TTS import speak

# 用来传递录音文件路径
audio_queue = queue.Queue()

def listen_loop():
    try:
        for path in record_audio():
            print(f"录音完成，放入队列: {path}")
            audio_queue.put(path)
    except Exception as e:
        print(f"[listen_loop] 异常: {e}")

def process_one_audio(path):
    try:
        print(f"开始识别: {path}")
        text = transcribe(path)
        print(f"识别内容：{text}")
        intent = get_intent(text)
        print(f"控制意图：{intent}")
        control_device(intent)
        reply = f"主人，{intent['设备']}已{intent['操作']}"
        speak(reply)
    except Exception as e:
        print(f"[process_one_audio] 异常: {e}")

def process_loop():
    try:
        while True:
            path = audio_queue.get()
            if path:
                p = multiprocessing.Process(target=process_one_audio, args=(path,))
                p.start()
                p.join()  # 可选：是否等待该任务完成后再处理下一个
    except Exception as e:
        print(f"[process_loop] 异常: {e}")

# 启动两个线程
if __name__ == "__main__":
    multiprocessing.freeze_support()  # 如果打包成 exe，推荐保留
    threading.Thread(target=process_loop, daemon=True).start()
    threading.Thread(target=listen_loop, daemon=True).start()
    
    print("启动,Ctrl+C 退出")

    try:
        while True:
            time.sleep(0.1)  # 主线程低功耗运行
    except KeyboardInterrupt:
        print("再见主人")
