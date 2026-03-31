import streamlit as st
import random

# 1. 页面配置
st.set_page_config(page_title="乌鸦喝水：竞技联动版", layout="wide")

# --- 音效函数 ---
def play_sound(sound_type):
    # 使用 GitHub 上的公开音效链接（你也可以换成自己的）
    sounds = {
        "stone": "https://www.soundjay.com/buttons/sounds/button-37.mp3", # 投石声
        "win": "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3", # 中奖/满水声
        "box": "https://www.soundjay.com/buttons/sounds/button-09.mp3"   # 开盒声
    }
    sound_html = f"""
        <audio autoplay>
            <source src="{sounds[sound_type]}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(sound_html, height=0)

# 2. 初始化状态
if 'scores' not in st.session_state:
    st.session_state.scores = {i: 0 for i in range(1, 7)}
if 'log' not in st.session_state:
    st.session_state.log = "游戏开始！"

# 3. 样式美化
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }
    .reportview-container { background: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# 4. 主界面布局
st.title("🦅 乌鸦喝水：全能竞技场")
st.info(f"📜 最近战报：{st.session_state.log}")

# --- 乌鸦喝水区 ---
cols = st.columns(6)
for i in range(1, 7):
    with cols[i-1]:
        st.subheader(f"第 {i} 组")
        score = st.session_state.scores[i]
        st.progress(score / 100)
        st.metric("水位", f"{score}%")
        
        if st.button(f"手动投石 🪨", key=f"add_{i}"):
            st.session_state.scores[i] = min(100, score + 10)
            play_sound("stone")
            if st.session_state.scores[i] >= 100:
                play_sound("win")
                st.balloons()
            st.rerun()

st.markdown("---")

# --- 联动盲盒区 ---
st.header("🎁 策略盲盒 (联动水位)")
st.write("点击盲盒抽取道具，直接影响各组水位！")

# 联动道具池
prizes = [
    {"name": "🌊 洪峰爆发", "effect": "本组水位 +20%", "type": "self", "value": 20},
    {"name": "🧊 结冰停滞", "effect": "任选对手组 -10%", "type": "target", "value": -10},
    {"name": "🌪️ 飓风来袭", "effect": "全场其他组 -5%", "type": "all_others", "value": -5},
    {"name": "💎 黄金巨石", "effect": "本组水位直接 +30%", "type": "self", "value": 30},
    {"name": "💀 漏水事故", "effect": "本组水位 -10% (惨)", "type": "self", "value": -10},
    {"name": "🔄 乾坤大挪移", "effect": "本组与第一名交换水位", "type": "swap", "value": 0}
]

box_cols = st.columns(4)
for i in range(8):
    with box_cols[i % 4]:
        if st.button(f"📦 神秘盲盒 {i+1}", key=f"box_{i}"):
            play_sound("box")
            item = random.choice(prizes)
            
            # 这里的逻辑：老师可以根据抽到的内容手动调整，或者通过下拉框选择目标
            st.warning(f"结果：{item['name']}!")
            st.write(item['effect'])
            
            # 记录战报
            st.session_state.log = f"某组抽到了【{item['name']}】，效果：{item['effect']}"
            
            # 自动执行简单的加减（默认加给对应操作组，复杂操作老师手动点投石）
            if item['type'] == "self":
                st.info("请老师手动为该组调整对应水位")

# 5. 重置按钮
if st.sidebar.button("清空重置游戏"):
    st.session_state.scores = {i: 0 for i in range(1, 7)}
    st.session_state.log = "游戏已重置"
    st.rerun()