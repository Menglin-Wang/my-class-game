import streamlit as st
import random
import time

# 1. 页面设置：全屏布局
st.set_page_config(page_title="智慧课堂：乌鸦喝水", layout="wide")

# 2. 注入多巴胺配色 CSS
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }
    div[data-testid="stMetricValue"] { color: #4facfe; font-size: 36px; }
    .stButton>button { width: 100%; border-radius: 20px; border: 2px solid #4facfe; }
    </style>
    """, unsafe_allow_html=True)

# 3. 初始化数据
if 'scores' not in st.session_state:
    st.session_state.scores = {i: 0 for i in range(1, 7)}
if 'boxes' not in st.session_state:
    st.session_state.boxes = {}

# 4. 侧边栏：扫码加入区域
with st.sidebar:
    st.header("📱 学生加入")
    # 获取当前页面的 URL
    current_url = "https://share.streamlit.io/" # 部署后会自动更新
    st.write("请学生扫描对应小组二维码：")
    
    selected_g = st.selectbox("选择生成哪组的码？", [f"第{i}组" for i in range(1, 7)])
    g_num = selected_g.replace("第","").replace("组","")
    
    # 模拟生成二维码（Streamlit Cloud 部署后可配合参数）
    st.info(f"💡 建议打印：{current_url}?group={g_num}")
    
    if st.button("🔥 重置全场比赛"):
        st.session_state.scores = {i: 0 for i in range(1, 7)}
        st.session_state.boxes = {}
        st.rerun()

# 5. 主界面：乌鸦喝水竞赛 (6个瓶子)
st.title("🦅 乌鸦喝水：小组积分实时赛")
cols = st.columns(6)

for i in range(1, 7):
    with cols[i-1]:
        st.markdown(f"### 🚩 第 {i} 组")
        score = st.session_state.scores[i]
        
        # 视觉进度条
        st.progress(score / 100)
        st.metric("水位", f"{score}%")
        
        if st.button(f"投石 🪨", key=f"add_{i}"):
            if score < 100:
                st.session_state.scores[i] += 10
                if st.session_state.scores[i] >= 100:
                    st.balloons()
            st.rerun()

st.markdown("---")

# 6. 底部：九宫格盲盒
st.header("🎁 课堂惊喜盲盒")
prizes = ["🌟 SSR:平时分满分", "🛡️ 复活甲", "⚡ 下题双倍", "🔄 换位卡", "➕ 积分+5", "➕ 积分+2", "🍭 颗糖果", "❌ 谢谢参与"]

box_cols = st.columns(4)
for i in range(8):
    with box_cols[i % 4]:
        if i not in st.session_state.boxes:
            if st.button(f"📦 盲盒 {i+1}", key=f"box_{i}"):
                st.session_state.boxes[i] = random.choice(prizes)
                st.rerun()
        else:
            st.success(st.session_state.boxes[i])