import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# Home Assistant配置
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN", "")
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123")

# 验证必要的配置
if not DEEPSEEK_API_KEY:
    print("警告: DEEPSEEK_API_KEY未设置，请在.env文件中配置")
if not HOME_ASSISTANT_TOKEN:
    print("警告: HOME_ASSISTANT_TOKEN未设置，请在.env文件中配置")
