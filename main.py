import threading
import queue
import time
import multiprocessing
import asyncio

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
        
        # 检查是否为无效指令或错误
        if intent == "无效指令" or "error" in intent:
            print("无效指令，继续处理下一条...")
            return
            
        # 执行有效指令
        control_device(intent)
        reply = f"主人，{intent['设备']}已{intent['操作']}"
        speak(reply)
    except Exception as e:
        print(f"[process_one_audio] 异常: {e}")

# 添加一个队列用于存放识别结果
result_queue = queue.Queue()

async def process_audio_async(path):
    try:
        print(f"开始识别: {path}")
        text = await asyncio.to_thread(transcribe, path)
        print(f"识别内容：{text}")
        result_queue.put(text)
    except Exception as e:
        print(f"[process_audio_async] 异常: {e}")

def handle_result():
    try:
        while True:
            text = result_queue.get()
            intent = get_intent(text)
            print(f"控制意图：{intent}")
            
            # 检查是否为无效指令或错误
            if intent == "无效指令" or "error" in intent:
                print("无效指令，继续处理下一条...")
                continue
            
            # 执行有效指令    
            control_device(intent)
            reply = f"主人，{intent['设备']}已{intent['操作']}"
            speak(reply)
    except Exception as e:
        print(f"[handle_result] 异常: {e}")

def process_loop():
    try:
        async def main():
            while True:
                path = audio_queue.get()
                if path:
                    await process_audio_async(path)
        asyncio.run(main())
    except Exception as e:
        print(f"[process_loop] 异常: {e}")

# 启动三个线程
if __name__ == "__main__":
    multiprocessing.freeze_support()  # 如果打包成 exe，推荐保留
    threading.Thread(target=process_loop, daemon=True).start()
    threading.Thread(target=listen_loop, daemon=True).start()
    threading.Thread(target=handle_result, daemon=True).start()
    
    print("启动,Ctrl+C 退出")

    try:
        while True:
            time.sleep(0.1)  # 主线程低功耗运行
    except KeyboardInterrupt:
        print("再见主人")
