#语音转文字

import whisper
from logger import setup_logger

logger = setup_logger("ASR")

# 使用medium模型，平衡速度和准确性
model = whisper.load_model("medium")  # 可选：tiny / base / small / medium / large

def transcribe(file_path):
    """
    将给定的音频文件转换为文本。

    使用预先训练好的模型将音频文件中的语音转换为文本。该函数的实现依赖于外部的模型，
    并假设模型已经被正确初始化和配置。

    参数:
    file_path (str): 音频文件的路径。字符串，指向待转换的音频文件。

    返回:
    str: 转换后的文本。如果转换过程中出现错误，应该在控制台打印错误信息。
    """
    # 使用模型转换音频文件
    logger.info(f"开始语音识别: {file_path}")
    result = model.transcribe(file_path, language='zh')
    text = result['text'].strip()
    logger.info(f"识别结果: {text}")
    return text

