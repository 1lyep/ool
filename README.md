# ool
---
## README结构
- 简介(https://github.com/1lyep/ool#%E7%AE%80%E4%BB%8B)
- 项目结构(https://github.com/1lyep/ool#%E9%A1%B9%E7%9B%AE%E7%BB%93%E6%9E%84)
- 各模块功能(https://github.com/1lyep/ool#%E5%90%84%E6%A8%A1%E5%9D%97%E5%8A%9F%E8%83%BD)
- 环境要求与配置(https://github.com/1lyep/ool#%E7%8E%AF%E5%A2%83%E8%A6%81%E6%B1%82%E4%B8%8E%E9%85%8D%E7%BD%AE)
---
>## 简介
#### 一个语音助手
---
>## 项目结构
```bash
ool
|ASR.py 语音转文字
|config.py 配置文件
|control.py 控制homeassistant
|hamap.py homeassistant设备和操作映射
|LLM.py 语义处理
|main.py 主入口与线程处理
|README.md 说明
|requirements.txt 依赖
|TTS.py 文本转语音
|VAD.py 语音检测机制
|voice 录音存放文件（需改进）
||audioxxxxx.wav
|out.mp3 输出音频
```
---
>## 各模块功能

---
>## 环境要求与配置
### 环境要求（本项目运行环境，没考虑其他可兼容环境）
目前为api版本需要联网  
24H2 x64 win11  
需要麦克风  
需手动创建一个“voice”文件夹用于存放录音文件  
python3.11.3
- python官网下载地址：  
[Windows installer (64-bit)](https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe)   
[Windows installer (32-bit)](https://www.python.org/ftp/python/3.11.3/python-3.11.3.exe)

需要安装ffmpeg
- 手动安装
[ffmpeg](https://ffmpeg.org/download.html#build-windows)  
[CSDN教程](https://blog.csdn.net/Natsuago/article/details/143231558)
- 命令行

Scoop
```bash
scoop install ffmpeg
```
Chocolatey
```bash
choco install ffmpeg
```

### 安装依赖
- 当创建并部署好项目后，进入到项目目录下，执行以下命令
```bash
pip install -r requirements.txt 
```
- 或根据**reuquirements.txt**中的依赖包手动安装
