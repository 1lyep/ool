import json
import os
from datetime import datetime
from logger import setup_logger

logger = setup_logger("HISTORY")

HISTORY_FILE = "command_history.json"

def save_command(text, intent, success=True):
    """
    保存命令历史记录
    
    参数:
    text: 识别的文本
    intent: 解析的意图
    success: 是否成功执行
    """
    if not os.path.exists(HISTORY_FILE):
        history = []
    else:
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
    
    record = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "text": text,
        "intent": intent,
        "success": success
    }
    
    history.append(record)
    
    # 只保留最近100条记录
    if len(history) > 100:
        history = history[-100:]
    
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存历史记录失败: {e}")

def get_recent_commands(limit=10):
    """
    获取最近的命令历史
    
    参数:
    limit: 返回的记录数量
    
    返回:
    list: 命令历史列表
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return history[-limit:]
    except Exception as e:
        logger.error(f"读取历史记录失败: {e}")
        return []

def clear_history():
    """清空历史记录"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            logger.info("历史记录已清空")
            return True
        return False
    except Exception as e:
        logger.error(f"清空历史记录失败: {e}")
        return False

