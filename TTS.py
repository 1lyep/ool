
# 语音合成

import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play

async def async_speak(text):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save("out.mp3")

    sound = AudioSegment.from_mp3("out.mp3")
    play(sound)

def speak(text):
    asyncio.run(async_speak(text))

