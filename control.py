
# 控制homeassistant

import requests
from config import HOME_ASSISTANT_TOKEN, HOME_ASSISTANT_URL
from hamap import DEVICE_MAP,ACTION_MAP
from logger import setup_logger

logger = setup_logger("CONTROL")

def control_device(intent):
    """
    根据用户意图控制设备

    此函数通过发送HTTP请求到Home Assistant API来控制设备的开关
    它根据传入的intent字典中包含的设备名称和动作来执行相应的控制操作

    参数:
    intent (dict): 包含用户意图的信息，包括设备名称和所需的动作
    """
    # 设置请求Home Assistant API所需的头部信息，包括认证令牌和内容类型
    headers = {
        "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json"
    }

    # 从intent中提取设备名称和动作
    entity = intent["设备"]
    action = intent["操作"]
    # 假设所有设备都是灯，因此domain为"light"

    # 从操作映射表获取操作名称
    service = ACTION_MAP.get(action)
    # 从设备映射表获取设备id
    entity_id = DEVICE_MAP.get(entity)

    # 提取 domain，例如 light.guadeng -> light
    domain = entity_id.split(".")[0]

    # 构造请求URL
    url = f"{HOME_ASSISTANT_URL}/api/services/{domain}/{service}"
    # 准备请求数据，指定要控制的设备
    data = {"entity_id": entity_id}

    # 发送POST请求到Home Assistant API
    try:
        r = requests.post(url, headers=headers, json=data, timeout=5)
        logger.info(f"控制结果: {r.status_code}")
        if r.status_code == 200:
            logger.info(f"设备控制成功: {entity} - {action}")
        else:
            logger.warning(f"设备控制失败: {entity} - {action}, 状态码: {r.status_code}")
        return r.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error(f"控制设备时发生错误: {e}")
        return False

