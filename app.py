import streamlit as st
import os
import json
from mac_image_clicker import MacImageClicker
from PIL import Image
import pyautogui
import glob
import datetime
import subprocess
import shutil
import time

st.set_page_config(page_title="图像点击任务助手（v10.1）", layout="wide")
st.title("🗂️ 图像点击任务助手（v1）")

ASSET_DIR = os.path.abspath("assets")
FLOW_DIR = os.path.abspath("data")
os.makedirs(ASSET_DIR, exist_ok=True)
os.makedirs(FLOW_DIR, exist_ok=True)

# 初始化 session 状态
if "selected_flow" not in st.session_state:
    st.session_state.selected_flow = "-- 不加载 --"

if "imported_tasks" not in st.session_state:
    st.session_state.imported_tasks = []

# ===== 侧边栏：流程选择 =====
st.sidebar.header("📂 流程管理")
json_files = [f for f in os.listdir(FLOW_DIR) if f.endswith(".json")]
flow_options = ["-- 不加载 --"] + json_files

selected_flow = st.sidebar.selectbox(
    "选择已有流程模板",
    flow_options,
    index=flow_options.index(st.session_state.selected_flow) if st.session_state.selected_flow in flow_options else 0
)

# 切换流程逻辑
if selected_flow != "-- 不加载 --" and selected_flow != st.session_state.selected_flow:
    try:
        with open(os.path.join(FLOW_DIR, selected_flow), "r", encoding="utf-8") as f:
            st.session_state.imported_tasks = json.load(f)
            st.session_state.selected_flow = selected_flow
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"❌ 加载失败: {e}")
elif selected_flow == "-- 不加载 --" and st.session_state.selected_flow != "-- 不加载 --":
    st.session_state.selected_flow = "-- 不加载 --"
    st.session_state.imported_tasks = []
    st.rerun()

# ===== 📸 系统截图 =====
st.subheader("📸 使用系统截图工具选取区域")
if st.button("🖼️ 框选截图（macOS 原生截图工具）"):
    try:
        temp_path = os.path.expanduser("~/Desktop/capture.png")
        subprocess.call(["screencapture", "-i", temp_path])
        time.sleep(0.5)
        if os.path.exists(temp_path):
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_path = os.path.join(ASSET_DIR, f"capture_gui_{ts}.png")
            shutil.move(temp_path, new_path)
            st.success(f"✅ 截图成功：{new_path}")
            st.image(new_path, width=300)
        else:
            st.warning("未完成截图或取消了操作")
    except Exception as e:
        st.error(f"截图失败：{e}")

# ===== 图像任务配置区 =====
st.subheader("🧩 配置每张图的执行次数")
png_files = sorted(glob.glob(os.path.join(ASSET_DIR, "*.png")))
selected_tasks = []

# 创建导入任务路径映射
imported_map = {}
for task in st.session_state.imported_tasks:
    path = task["image_path"]
    imported_map[path] = imported_map.get(path, 0) + 1

cols = st.columns(4)
for i, file in enumerate(png_files):
    default_checked = file in imported_map
    default_count = imported_map.get(file, 0)
    with cols[i % 4]:
        inner_cols = st.columns([1, 1.2])
        with inner_cols[0]:
            st.image(file, width=100)
        with inner_cols[1]:
            checked = st.checkbox("选择", key=f"chk_{file}", value=default_checked)
            if checked:
                count = st.number_input("执行次数", min_value=1, value=default_count if default_count else 1, step=1, key=f"count_{file}")
                selected_tasks.append({
                    "name": os.path.basename(file),
                    "image_path": file,
                    "offset": (0, 0),
                    "count": count
                })

# ===== 导出流程 =====
st.subheader("📤 导出任务流程为 JSON")
if selected_tasks:
    export_data = []
    for task in selected_tasks:
        for _ in range(task.get("count", 1)):
            export_data.append({
                "name": task["name"],
                "image_path": task["image_path"],
                "offset": task["offset"]
            })

    json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
    st.download_button("💾 下载当前任务 JSON", data=json_str, file_name="task_plan.json", mime="application/json")

    new_name = st.text_input("另存为流程文件名（不含扩展名）", value="new_flow")
    if st.button("💾 保存流程到 data/ 目录"):
        save_path = os.path.join(FLOW_DIR, f"{new_name}.json")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        st.session_state.selected_flow = f"{new_name}.json"
        st.success(f"✅ 已保存流程为：{save_path}")
        st.rerun()

# ===== 偏移设置 =====
st.subheader("🧭 全局偏移设置")
offset_x = st.number_input("统一 X 偏移", value=0)
offset_y = st.number_input("统一 Y 偏移", value=0)

# ===== ▶️ 执行任务 =====
if st.button("▶️ 执行所有任务"):
    if not selected_tasks:
        st.warning("请至少选择一张图片")
    else:
        clicker = MacImageClicker()
        for task in selected_tasks:
            for i in range(task.get("count", 1)):
                st.write(f"执行：{task['name']}（第 {i+1} 次）")
                result = clicker.run_task(
                    name=task['name'],
                    image_path=task['image_path'],
                    offset=(offset_x, offset_y)
                )
                if result:
                    st.success(f"✅ 点击成功：{task['name']}")
                else:
                    st.error(f"❌ 点击失败：{task['name']}")
