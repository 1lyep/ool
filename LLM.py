import requests
import json
from config import DEEPSEEK_API_KEY

def get_intent(text):
    """
    根据用户输入的文本解析出指令意图，包括设备和操作类型。
    
    参数:
    text (str): 用户输入的指令文本。
    
    返回:
    dict: 包含设备和操作类型的字典，如{"device": "客厅灯", "action": "打开"}。
           如果解析失败，返回包含错误信息的字典，如{"error": "指令解析失败，请重新输入"}。
    """
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    # 结构化Prompt模板
    prompt = f"""你是一个专业家居助手,请严格按JSON格式解析用户指令:

    用户指令："{text}"

    解析要求：
    1. 识别设备名称：仅限["挂灯","空调"]
    2. 识别操作类型：["打开", "关闭", "调高", "调低","调暗","调亮"]
    4. 若说话与控制家居设备无关，请返回"无效指令"

    示例输出：
    {{"设备": "空调", "操作": "调高"}}"""
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",  # 根据需求选择模型
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,  # 降低随机性保证格式稳定
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
        
        print("收到回复内容：", content)
        # 清除 markdown 包裹
        if content.startswith("```"):
            content = content.strip("`")  # 去掉所有 ` 符号
            content = content.strip("json")  # 如果有标注类型也清掉
            content = content.strip()
        print("收到回复内容：", content)
        
        # 安全解析JSON
        parsed = json.loads(content)
        
        # 添加字段验证
        valid_devices = {"挂灯","空调"}
        valid_do = {"打开", "关闭", "调高", "调低","调暗","调亮"}
        if parsed.get("设备") not in valid_devices or parsed.get("操作") not in valid_do:
            raise ValueError("无效")
        
        return parsed
        
    except (requests.exceptions.RequestException, 
            json.JSONDecodeError, 
            KeyError,
            ValueError) as error:
        # 错误处理
        print(f"111指令解析失败: {str(error)}")
        return {"error": "指令解析失败，请重新输入"}