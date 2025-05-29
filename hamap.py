
# 设备和操作的映射

# 中文设备名 到 HA 实体 ID 的映射
DEVICE_MAP = {
    "挂灯": "light.guadeng",
    "电脑灯": "light.guadeng",
    "空调":"light.guadeng"
    # 可以继续扩展
}

# 中文动作 到 HA 服务名的映射
ACTION_MAP = {
    "打开": "turn_on",
    "关闭": "turn_off",
    "调高": "turn_on",
    "调低": "turn_off",
    "调暗": "turn_off",
    "调亮": "turn_on",
    
    # 可以继续扩展
}
