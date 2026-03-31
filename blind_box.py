import streamlit as st
import random

st.set_page_config(page_title="课堂惊喜盲盒", layout="centered")

def play_box_sound():
    # 开箱音效：稍微欢快清脆的声音
    sound_url = "https://www.w3school.com.cn/i/song.mp3"
    js = f"""<script>var audio = new Audio("{sound_url}"); audio.play(); setTimeout(()=>{{audio.pause(); audio.currentTime=0;}}, 1000);</script>"""
    st.components.v1.html(js, height=0)

if 'box_results' not in st.session_state:
    st.session_state.box_results = {}

st.title("🎁 课堂策略盲盒")
st.info("当小组达成阶段成就或表现优异时，开启神秘道具！")

prizes = [
    "🌊 涌泉：本组水位 +15%", "🌪️ 狂风：对手全员 -5%", 
    "🧊 冰封：指定一组 -10%", "💎 巨石：本组水位 +25%",
    "🔄 交换：与最高分交换水位", "🛡️ 护盾：抵消下次扣分"
]

# 3x3 盲盒矩阵
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        with cols[col]:
            if idx not in st.session_state.box_results:
                if st.button(f"📦 盒子 {idx+1}", key=f"box_{idx}", use_container_width=True):
                    play_box_sound()
                    st.session_state.box_results[idx] = random.choice(prizes)
                    st.rerun()
            else:
                st.success(st.session_state.box_results[idx])

if st.button("🔄 刷新盲盒墙"):
    st.session_state.box_results = {}
    st.rerun()