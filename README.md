# 🖱️ 图像自动点击助手 V1 - 发布版

一个基于 Streamlit + OpenCV + pyautogui 的**图像识别自动点击工具**，支持流程式配置、批量执行、多流程管理、原生截图等功能。
Asset 资源截图请保存为 png 格式

---

## 📁 项目结构

```
image_clicker_gui/
├── app.py                    # Streamlit 主程序（图形化配置流程）
├── mac_image_clicker.py      # 图像识别与点击逻辑组件
├── requirements.txt          # 依赖列表（含版本号）
├── start.sh                  # 一键启动脚本（自动安装并运行）
├── project_structure.md      # 项目结构说明
├── assets/                   # 存放上传截图（点击目标图像）
├── data/                     # 存储导入导出的流程 JSON 文件
```

---

## 🚀 快速开始

### ✅ 第一次运行：

```bash
bash start.sh
```

它将会：

-   自动创建虚拟环境 `.venv`
-   安装依赖
-   启动 `app.py`（Streamlit 图形界面）

浏览器自动打开地址：http://localhost:8501

---

## ✨ 核心功能（V1）

| 功能                    | 描述                                             |
| ----------------------- | ------------------------------------------------ |
| ✅ 图像识别 + 点击执行  | 使用模板图匹配目标位置后偏移点击                 |
| ✅ 原生截图（macOS）    | 支持 `screencapture -i` 框选截图保存到 `assets/` |
| ✅ 多任务流程编辑       | 图像支持多次执行 + 排列展示                      |
| ✅ 流程导入导出（JSON） | 支持任务流程持久化保存 / 加载                    |
| ✅ 多流程切换（data/）  | 可存储多个 JSON 流程文件，页面侧栏选择           |
| ✅ 失败重试机制         | 每步最多尝试匹配 3 次                            |
| ✅ 页面配置状态保持     | 流程加载后自动勾选图像 + 还原执行次数            |

---

## 📂 JSON 流程格式示例

```json
[
	{
		"name": "点击登录按钮",
		"image_path": "assets/button_login.png",
		"offset": [10, 10]
	},
	{
		"name": "点击确定",
		"image_path": "assets/button_ok.png",
		"offset": [0, 0]
	}
]
```

---

## 📦 依赖版本（requirements.txt）

```txt
streamlit>=1.30
pyautogui>=0.9.53
opencv-python>=4.8.0
Pillow>=9.0.0
```

建议使用 Python 3.9~3.10 运行。

---

## 🧩 后续可扩展方向（V2 划规建议）

TOOD 欢迎 issue 讨论

---

## 📄 版权与许可

本工具由开发者自用开发，未绑定平台账户，后续如需商业用途可另行处理授权方式。
