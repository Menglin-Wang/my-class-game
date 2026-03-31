import streamlit as st

st.set_page_config(page_title="乌鸦喝水-小组竞赛", layout="wide")

# 自定义 CSS：让进度条更像水瓶
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-image: linear-gradient(to top, #4facfe 0%, #00f2fe 100%); height: 30px; }
    .group-container { border: 2px solid #e6e9ef; padding: 15px; border-radius: 15px; text-align: center; background: white; }
    </style>
    """, unsafe_allow_html=True)

def play_crow_sound():
    # 投石音效：短促的“滴”或“咚”
    sound_url = "https://www.w3school.com.cn/i/horse.ogg" 
    js = f"""<script>var audio = new Audio("{sound_url}"); audio.currentTime = 0.5; audio.play(); setTimeout(()=>{{audio.pause();}}, 400);</script>"""
    st.components.v1.html(js, height=0)

if 'scores' not in st.session_state:
    st.session_state.scores = {i: 0 for i in range(1, 7)}

st.title("🦅 乌鸦喝水：小组积分竞赛")
st.write("答对题目投下一颗石子，看哪组乌鸦先喝到水！")

cols = st.columns(6)
for i in range(1, 7):
    with cols[i-1]:
        st.markdown(f"<div class='group-container'><h3>第 {i} 组</h3>", unsafe_allow_html=True)
        score = st.session_state.scores[i]
        st.progress(score / 100)
        st.metric("水位", f"{score}%")
        
        if st.button(f"🪨 投石", key=f"crow_{i}"):
            st.session_state.scores[i] = min(100, score + 10)
            play_crow_sound()
            if st.session_state.scores[i] >= 100:
                st.balloons()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

if st.sidebar.button("🔄 重置所有水位"):
    st.session_state.scores = {i: 0 for i in range(1, 7)}
    st.rerun()