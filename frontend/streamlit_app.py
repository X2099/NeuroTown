import base64
import random
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

API_BASE = "http://127.0.0.1:8000/"

# ---------------- 页面配置 ---------------- #
st.set_page_config(page_title="神经小镇 Live", page_icon="🏡", layout="wide")

# ---------------- 自动刷新 ---------------- #
st_autorefresh(interval=5000, key="auto_refresh")  # 每 2 秒刷新一次页面

# ---------------- 初始化状态 ---------------- #
if "tick" not in st.session_state:
    st.session_state.tick = 0
if "weather" not in st.session_state:
    st.session_state.weather = random.choice(["☀️ 晴", "🌥️ 阴", "🌧️ 小雨", "❄️ 大雪"])
if "npcs" not in st.session_state:
    # 默认空列表，后续每次刷新从后端拉取
    st.session_state.npcs = []

MOOD_COLORS = {
    "开心": "#fff6bf",
    "好奇": "#d7f9f3",
    "疲倦": "#f3d7d7"
}


# ---------------- CSS 样式 ---------------- #
def set_bg(local_image_path):
    with open(local_image_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    .town-map {{
    position: relative;
    width: 1228.8px;
    height: 819.2px;
    background: url("data:image/png;base64,{b64}") center/cover no-repeat;
    border-radius: 25px;
    margin: 10px auto;
    overflow: visible;
    border: 4px solid #f0d7b3;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


set_bg("frontend/assets/bg_town.png")

st.markdown("""
<style>
body {
    background-color: #fffaf2;
}
.npc {
    position: absolute;
    transition: all 1.5s ease-in-out;
}
.avatar {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    text-align: center;
    font-size: 32px;
    line-height: 60px;
    background-color: #fff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    border: 2px solid white;
}

.bubble {
    position: absolute;
    top: -150px; /* 让气泡显示在头像上方 */
    left: -10px;
    width: 110px;
    background: rgba(255,255,255,0.9);
    border-radius: 12px;
    font-size: 13px;
    padding: 6px 10px;
    text-align: left;
    line-height: 1.2;       /* 行间距调小，可以改成 1.1 或 1.3 根据喜好 */
    word-wrap: break-word;  /* 超长文字自动换行 */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    animation: fadeIn 0.8s ease-in-out;
}
.name {
    margin: 0;
    padding: 0;
    font-size: 12px;
    color: #000;
}
@keyframes fadeInOut {
    0% {opacity: 0;}
    10% {opacity: 1;}
    90% {opacity: 1;}
    100% {opacity: 0;}
}
</style>
""", unsafe_allow_html=True)

# ---------------- 顶部状态 ---------------- #
st.markdown("""
    <style>
    /* 减小标题与顶部的距离 */
    .block-container {
        padding-top: 0rem; /* 默认大约是 6rem */
        margin-top: 0rem;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown(f"#### 🏡 神经小镇 Live  |  **🕒 第 {st.session_state.tick + 1} 天** | {st.session_state.weather}")

# ---------------- 控制按钮 ---------------- #
col1, col2, col3 = st.columns(3)

if col1.button("▶️ 推进时间"):
    try:
        requests.post(f"{API_BASE}/town/tick")
        st.session_state.tick += 1
        st.success("时间流动了一刻")
    except Exception as e:
        st.error(f"无法连接后端推进时间：{e}")

if col2.button("🌦️ 改变天气"):
    st.session_state.weather = random.choice(["☀️ 晴", "🌥️ 阴", "🌧️ 小雨", "❄️ 大雪"])
    st.success(f"天气改变为 {st.session_state.weather}")

if col3.button("🎲 随机事件"):
    if st.session_state.npcs:
        npc = random.choice(st.session_state.npcs)
        st.toast(f"💬 {npc['name']} {npc['action']}，看起来很{npc['mood']}！")

# ---------------- 地图显示 ---------------- #
html = '<div class="town-map">'

# 拉取 NPC 数据
try:
    npcs = requests.get(f"{API_BASE}/town/npcs").json()
    st.session_state.npcs = npcs
except Exception as e:
    st.error(f"❌ 无法连接后端接口: {e}")
    npcs = st.session_state.npcs  # 使用上一次缓存的数据

for npc in st.session_state.npcs:
    npc["x"] += random.randint(-10, 10)
    npc["y"] += random.randint(-10, 10)
    npc["x"] = max(0, min(95, npc["x"]))  # 边界限制
    npc["y"] = max(0, min(92, npc["y"]))
    # npc["x"] = 95  # 边界限制
    # npc["y"] = 92
    # break

for npc in npcs:
    color = MOOD_COLORS.get(npc.get("mood", ""), "#ffffff")
    texts = npc.get("memory", "").split('\n')
    html += f"""<div class="npc" style="left:{npc['x']}%;top:{npc['y']}%;">"""  # 位置
    html += f"""<div class="avatar" style="background-color:{color};">{npc['emoji']}<br><small class="name">{npc['name']}</small></div>"""
    html += f"""<div class="bubble">"""
    for text in texts:
        html += f"""<p style="margin-bottom: 2.5px;">{text}</p>"""
    html += "</div></div>"
st.markdown(html, unsafe_allow_html=True)
