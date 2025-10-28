# 语音合成

import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
from logger import setup_logger

logger = setup_logger("TTS")

async def async_speak(text):
    try:
        logger.info(f"生成语音: {text}")
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save("out.mp3")

        sound = AudioSegment.from_mp3("out.mp3")
        play(sound)
        logger.info("语音播放完成")
    except Exception as e:
        logger.error(f"语音合成失败: {e}")

def speak(text):
    asyncio.run(async_speak(text))

