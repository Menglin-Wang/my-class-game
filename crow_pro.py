import streamlit as st

st.set_page_config(page_title="乌鸦喝水-专业版", layout="wide")

# 1. 声音播放函数 (使用短促音效并强制循环触发)
def play_effect(sound_type):
    urls = {
        "stone": "https://www.w3schools.com/tags/horse.ogg", # 投石声
        "win": "https://www.w3schools.com/tags/movie.mp4"    # 达标声
    }
    js = f"""
        <script>
            var audio = new Audio("{urls[sound_type]}");
            audio.currentTime = 0.5; 
            audio.play();
            setTimeout(()=>{{ audio.pause(); }}, 600); // 0.6秒强制切断
        </script>
    """
    st.components.v1.html(js, height=0)

# 2. 初始化数据
if 'scores' not in st.session_state:
    st.session_state.scores = {i: 0 for i in range(1, 7)}

# 3. 顶部控制栏
st.title("🦅 乌鸦喝水：小组积分赛")
col_ctrl1, col_ctrl2 = st.columns([1, 4])
with col_ctrl1:
    if st.button("🔔 点击激活音效"):
        play_effect("stone")
        st.toast("音效已激活！")
with col_ctrl2:
    st.caption("提示：所有分值以10为单位。水位不设上限，看谁飞得最高！")

# 4. 比赛区域
cols = st.columns(6)
for i in range(1, 7):
    with cols[i-1]:
        st.subheader(f"第 {i} 组")
        score = st.session_state.scores[i]
        
        # 视觉进度：超过100后进度条保持满格颜色，但数值继续跳动
        display_progress = min(score, 100)
        st.progress(display_progress / 100)
        
        # 大字报分数
        st.metric("当前水位", f"{score}%", delta="↑" if score > 0 else None)
        
        # 操作按钮 (以10为单位)
        if st.button(f"🪨 投石 +10", key=f"add_{i}"):
            st.session_state.scores[i] += 10
            play_effect("stone")
            st.rerun()
        
        if st.button(f"💧 漏水 -10", key=f"sub_{i}"):
            st.session_state.scores[i] = max(0, st.session_state.scores[i] - 10)
            play_effect("stone")
            st.rerun()

if st.sidebar.button("🔄 重置所有分数"):
    st.session_state.scores = {i: 0 for i in range(1, 7)}
    st.rerun()