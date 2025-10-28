# 智能语音家居控制系统 (OOL)

## 📖 简介

一个基于语音的智能家居控制系统，通过语音识别和AI意图解析，实现对Home Assistant连接设备的语音控制。支持设备控制、状态查询、命令历史等功能。

## ✨ 特性

- 🎤 **智能语音识别**: 使用OpenAI Whisper模型，高精度中文识别
- 🤖 **AI意图解析**: 集成DeepSeek API，准确理解用户指令
- 🏠 **设备控制**: 通过Home Assistant控制智能家居设备
- 📢 **语音反馈**: 使用Edge-TTS提供中文语音回复
- 📝 **命令历史**: 记录最近100条操作历史
- 📊 **状态查询**: 实时查询设备状态
- 📋 **完善日志**: 多级别日志记录，便于调试

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Windows 10/11 (x64)
- 麦克风设备
- FFmpeg

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd ool
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **安装FFmpeg**

**Windows (Scoop)**:
```bash
scoop install ffmpeg
```

**Windows (Chocolatey)**:
```bash
choco install ffmpeg
```

**手动安装**: [FFmpeg下载](https://ffmpeg.org/download.html#build-windows)

4. **配置环境变量**

复制 `.env.example` 为 `.env` 并填写配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

# Home Assistant配置
HOME_ASSISTANT_URL=http://localhost:8123
HOME_ASSISTANT_TOKEN=your_token_here
```

5. **创建必要目录**
```bash
mkdir voice
mkdir logs
```

### 运行

```bash
python main.py
```

使用 `Ctrl+C` 退出程序

## 📁 项目结构

```
ool/
├── main.py              # 主程序入口
├── config.py           # 配置文件
├── logger.py           # 日志系统
├── VAD.py              # 语音活动检测
├── ASR.py              # 语音识别
├── LLM.py              # 意图识别
├── control.py          # 设备控制
├── status_query.py     # 状态查询
├── history.py          # 历史记录
├── TTS.py              # 语音合成
├── hamap.py            # 设备映射
├── requirements.txt    # 依赖列表
├── .env               # 环境变量（需创建）
└── 季度报告.md         # 项目季度报告
```

## 🎯 使用说明

### 支持的操作

#### 1. 设备控制
- "打开挂灯"
- "关闭空调"
- "调亮挂灯"
- "调暗挂灯"
- "调高空调"
- "调低空调"

#### 2. 状态查询
- "查询挂灯状态"
- "挂灯现在怎么样"
- "空调状态"

#### 3. 历史记录
- "查看历史记录"
- "最近做了什么"
- "历史"

## 🔧 配置说明

### 设备映射

编辑 `hamap.py` 添加新设备：

```python
DEVICE_MAP = {
    "挂灯": "light.guadeng",
    "空调": "light.guadeng",
    # 添加更多设备...
}

ACTION_MAP = {
    "打开": "turn_on",
    "关闭": "turn_off",
    # 添加更多操作...
}
```

### 调整VAD参数

编辑 `VAD.py` 中的参数：

- `vad_threshold`: 能量阈值（默认0.02）
- `zcr_threshold`: 过零率阈值（默认0.3）
- `silence_limit`: 静音限制（默认2.0秒）

## 📊 日志系统

- 日志文件存放在 `logs/` 目录
- 按日期命名，自动创建
- 包含详细的时间戳和函数信息
- 支持DEBUG、INFO、WARNING、ERROR级别

## 🐛 故障排除

### 1. 麦克风无法识别

- 检查麦克风权限设置
- 确认麦克风是否正常工作
- 查看日志文件获取详细错误信息

### 2. API调用失败

- 检查网络连接
- 验证API密钥是否正确
- 查看控制台错误提示

### 3. 设备控制失败

- 检查Home Assistant连接
- 验证实体ID是否正确
- 查看Home Assistant日志

### 4. 识别准确率低

- 调整VAD参数
- 改善录音环境（减少噪音）
- 尝试使用Whisper large模型

## 📝 更新日志

### v1.1.0 (本季度)
- ✨ 新增完善的日志系统
- ✨ 新增命令历史记录功能
- ✨ 新增设备状态查询功能
- ✨ 支持多意图类型（控制/查询/历史）
- 🔧 改进配置文件管理（环境变量）
- 🔧 优化异常处理机制
- 📝 完善项目文档

### v1.0.0
- 🎉 初始版本发布
- 基础语音识别和控制功能

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请提交Issue或联系项目维护者。

