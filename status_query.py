import requests
from config import HOME_ASSISTANT_TOKEN, HOME_ASSISTANT_URL
from hamap import DEVICE_MAP
from logger import setup_logger

logger = setup_logger("STATUS_QUERY")

def get_device_status(device_name):
    """
    查询设备状态
    
    参数:
    device_name: 设备名称（中文）
    
    返回:
    dict: 设备状态信息，或None如果查询失败
    """
    entity_id = DEVICE_MAP.get(device_name)
    if not entity_id:
        logger.warning(f"未找到设备: {device_name}")
        return None
    
    url = f"{HOME_ASSISTANT_URL}/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            state = response.json()
            logger.info(f"设备状态查询成功: {device_name}")
            return state
        else:
            logger.warning(f"设备状态查询失败: {device_name}, 状态码: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"查询设备状态时发生错误: {e}")
        return None

def format_status_reply(state):
    """
    格式化状态回复信息
    
    参数:
    state: 设备状态字典
    
    返回:
    str: 格式化的状态信息
    """
    if not state:
        return "无法查询设备状态"
    
    device_name = state.get('attributes', {}).get('friendly_name', '设备')
    is_on = state.get('state') == 'on'
    
    if is_on:
        return f"{device_name}目前是开启状态"
    else:
        return f"{device_name}目前是关闭状态"

