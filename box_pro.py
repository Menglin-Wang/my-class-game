import streamlit as st
import random

st.set_page_config(page_title="策略盲盒-联动版", layout="centered")

def play_box_sound():
    url = "https://www.w3school.com.cn/i/song.mp3"
    js = f"""<script>var audio = new Audio("{url}"); audio.play(); setTimeout(()=>{{audio.pause(); audio.currentTime=0;}}, 800);</script>"""
    st.components.v1.html(js, height=0)

if 'boxes' not in st.session_state:
    st.session_state.boxes = {}

st.title("🎁 策略盲盒墙")
if st.button("🔔 激活/测试音效"):
    play_box_sound()

# 道具库：全部统一为 10 的倍数
prizes = [
    "🌊 涌泉：本组水位 +20%", 
    "🌪️ 狂风：除本组外全场 -10%", 
    "🧊 冰封：指定对手组 -20%", 
    "💎 巨石：本组水位 +30%",
    "💧 渗漏：本组水位 -10%",
    "🔄 逆转：与最高分那一组交换水位"
]

# 布局
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        with cols[col]:
            if idx not in st.session_state.boxes:
                if st.button(f"📦 盲盒 {idx+1}", key=f"box_{idx}", use_container_width=True):
                    play_box_sound()
                    st.session_state.boxes[idx] = random.choice(prizes)
                    st.rerun()
            else:
                st.success(st.session_state.boxes[idx])

if st.button("🔄 刷新盲盒"):
    st.session_state.boxes = {}
    st.rerun()