import requests
import json
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from logger import setup_logger

logger = setup_logger()

def get_intent(text):
    """
    根据用户输入的文本解析出指令意图，包括设备和操作类型。
    
    参数:
    text (str): 用户输入的指令文本。
    
    返回:
    dict: 包含设备和操作类型的字典，如果解析失败，返回包含错误信息的字典。
    """
    api_url = DEEPSEEK_API_URL
    
    # 结构化Prompt模板
    prompt = f"""你是一个专业家居助手,请严格按JSON格式解析用户指令:

    用户指令："{text}"

    解析要求：
    1. 识别意图类型：["控制", "查询", "历史"]
    2. 识别设备名称：仅限["挂灯","空调"]
    3. 识别操作类型（如果是控制）：["打开", "关闭", "调高", "调低","调暗","调亮"]
    4. 若说话与控制家居设备无关，请返回"无效指令"

    示例输出（控制）：
    {{"类型": "控制", "设备": "空调", "操作": "调高"}}

    示例输出（查询）：
    {{"类型": "查询", "设备": "挂灯"}}

    示例输出（查看历史）：
    {{"类型": "历史"}}"""
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 100
    }
    
    try:
        # API调用安全封装
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=8  # 设置超时时间
        )
        response.raise_for_status()  # 自动处理HTTP错误
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        logger.debug(f"收到回复内容：{content}")
        # 清除 markdown 包裹
        if content.startswith("```"):
            content = content.strip("`")  # 去掉所有 ` 符号
            content = content.strip("json")  # 如果有标注类型也清掉
            content = content.strip()
        logger.debug(f"清理后的内容：{content}")
        
        # 安全解析JSON
        parsed = json.loads(content)
        
        # 添加字段验证
        intent_type = parsed.get("类型", "")
        
        if intent_type == "历史":
            # 历史记录查询不需要验证设备
            return parsed
        elif intent_type == "查询":
            # 只验证设备
            valid_devices = {"挂灯", "空调"}
            if parsed.get("设备") not in valid_devices:
                raise ValueError("无效设备")
            return parsed
        elif intent_type == "控制":
            # 验证设备和操作
            valid_devices = {"挂灯", "空调"}
            valid_do = {"打开", "关闭", "调高", "调低", "调暗", "调亮"}
            if parsed.get("设备") not in valid_devices or parsed.get("操作") not in valid_do:
                raise ValueError("无效")
            return parsed
        else:
            raise ValueError("无效的意图类型")
        
    except (requests.exceptions.RequestException, 
            json.JSONDecodeError, 
            KeyError,
            ValueError) as error:
        # 错误处理
        logger.error(f"指令解析失败: {str(error)}")
        return {"error": "指令解析失败，请重新输入"}