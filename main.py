import threading
import queue
import time
import multiprocessing
import asyncio
from datetime import datetime

from VAD import record_audio  # 每次自动录一段
from ASR import transcribe
from LLM import get_intent
from control import control_device
from TTS import speak
from logger import setup_logger
from status_query import get_device_status, format_status_reply
from history import save_command, get_recent_commands

# 用来传递录音文件路径
audio_queue = queue.Queue()

# 初始化日志记录器
logger = setup_logger("MAIN")

def listen_loop():
    try:
        for path in record_audio():
            logger.info(f"录音完成，放入队列: {path}")
            audio_queue.put(path)
    except Exception as e:
        logger.error(f"[listen_loop] 异常: {e}", exc_info=True)

def process_one_audio(path):
    """处理单段音频（保留用于备用）"""
    try:
        logger.info(f"开始识别: {path}")
        text = transcribe(path)
        logger.info(f"识别内容：{text}")
        intent = get_intent(text)
        logger.info(f"解析意图：{intent}")
        
        # 检查是否为无效指令或错误
        if intent == "无效指令" or "error" in intent:
            logger.warning("无效指令，继续处理下一条...")
            save_command(text, intent, success=False)
            return
        
        intent_type = intent.get("类型", "")
        
        # 处理不同类型的意图
        if intent_type == "控制":
            success = control_device(intent)
            if success:
                reply = f"主人，{intent['设备']}已{intent['操作']}"
                speak(reply)
            else:
                reply = f"主人，{intent['设备']}控制失败"
                speak(reply)
            save_command(text, intent, success)
        elif intent_type == "查询":
            state = get_device_status(intent['设备'])
            if state:
                reply = format_status_reply(state)
                speak(reply)
                save_command(text, intent, success=True)
            else:
                speak("无法查询设备状态")
                save_command(text, intent, success=False)
        elif intent_type == "历史":
            commands = get_recent_commands(5)
            if commands:
                reply = "最近5条命令："
                for cmd in commands:
                    reply += f"\n{cmd['timestamp']}: {cmd['text']}"
                logger.info(reply)
                speak("主人，历史记录已显示在日志中")
            else:
                speak("没有历史记录")
            save_command(text, intent, success=True)
            
    except Exception as e:
        logger.error(f"[process_one_audio] 异常: {e}", exc_info=True)

# 添加一个队列用于存放识别结果
result_queue = queue.Queue()

async def process_audio_async(path):
    try:
        logger.info(f"开始识别: {path}")
        text = await asyncio.to_thread(transcribe, path)
        logger.info(f"识别内容：{text}")
        result_queue.put(text)
    except Exception as e:
        logger.error(f"[process_audio_async] 异常: {e}", exc_info=True)

def handle_result():
    try:
        while True:
            text = result_queue.get()
            intent = get_intent(text)
            logger.info(f"解析意图：{intent}")
            
            # 检查是否为无效指令或错误
            if intent == "无效指令" or "error" in intent:
                logger.warning("无效指令，继续处理下一条...")
                save_command(text, intent, success=False)
                continue
            
            intent_type = intent.get("类型", "")
            
            # 处理不同类型的意图
            if intent_type == "控制":
                # 控制设备
                success = control_device(intent)
                if success:
                    reply = f"主人，{intent['设备']}已{intent['操作']}"
                    speak(reply)
                else:
                    reply = f"主人，{intent['设备']}控制失败"
                    speak(reply)
                save_command(text, intent, success)
                
            elif intent_type == "查询":
                # 查询设备状态
                state = get_device_status(intent['设备'])
                if state:
                    reply = format_status_reply(state)
                    speak(reply)
                    save_command(text, intent, success=True)
                else:
                    speak("无法查询设备状态")
                    save_command(text, intent, success=False)
                    
            elif intent_type == "历史":
                # 查看历史记录
                commands = get_recent_commands(5)
                if commands:
                    reply = "最近5条命令："
                    for cmd in commands:
                        reply += f"\n{cmd['timestamp']}: {cmd['text']}"
                    logger.info(reply)
                    speak("主人，历史记录已显示在日志中")
                else:
                    speak("没有历史记录")
                save_command(text, intent, success=True)
            else:
                logger.warning(f"未知的意图类型: {intent_type}")
                
    except Exception as e:
        logger.error(f"[handle_result] 异常: {e}", exc_info=True)

def process_loop():
    try:
        async def main():
            while True:
                path = audio_queue.get()
                if path:
                    await process_audio_async(path)
        asyncio.run(main())
    except Exception as e:
        logger.error(f"[process_loop] 异常: {e}", exc_info=True)

# 启动三个线程
if __name__ == "__main__":
    multiprocessing.freeze_support()  # 如果打包成 exe，推荐保留
    threading.Thread(target=process_loop, daemon=True).start()
    threading.Thread(target=listen_loop, daemon=True).start()
    threading.Thread(target=handle_result, daemon=True).start()
    
    logger.info("语音助手启动,Ctrl+C 退出")

    try:
        while True:
            time.sleep(0.1)  # 主线程低功耗运行
    except KeyboardInterrupt:
        logger.info("再见主人")
        print("再见主人")
