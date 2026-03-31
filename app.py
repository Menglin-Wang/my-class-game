import streamlit as st
import random

st.set_page_config(page_title="乌鸦喝水联动版", layout="wide")

# --- 优化后的短促音效逻辑 ---
def play_short_sound(action):
    # 使用更短促的音效地址
    sound_urls = {
        "stone": "https://www.w3schools.com/tags/horse.ogg", # 示例，实际会通过JS截断
        "win": "https://www.w3schools.com/tags/movie.mp4",
        "box": "https://www.w3school.com.cn/i/song.mp3"
    }
    
    # JavaScript 逻辑：播放 0.8 秒后自动停止并重置
    js_code = f"""
        <script>
            var audio = new Audio("{sound_urls.get(action)}");
            audio.play();
            setTimeout(function(){{
                audio.pause();
                audio.currentTime = 0;
            }}, 800); // 800毫秒后强制停止，你可以根据需要改成 500
        </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 初始化数据 ---
if 'scores' not in st.session_state:
    st.session_state.scores = {i: 0 for i in range(1, 7)}
if 'log' not in st.session_state:
    st.session_state.log = "游戏开始！"

# --- 侧边栏 ---
with st.sidebar:
    st.title("⚙️ 课堂设置")
    st.warning("📣 上课前请先点击下方按钮激活音效权限")
    if st.button("🔔 激活并测试短音效"):
        play_short_sound("stone")
    
    st.divider()
    if st.button("🔄 重置比赛"):
        st.session_state.scores = {i: 0 for i in range(1, 7)}
        st.session_state.log = "数据已重置"
        st.rerun()

# --- 主界面 ---
st.title("🦅 乌鸦喝水：竞技场")
st.info(f"🚩 战报：{st.session_state.log}")

cols = st.columns(6)
for i in range(1, 7):
    with cols[i-1]:
        st.subheader(f"第 {i} 组")
        score = st.session_state.scores[i]
        st.progress(score / 100)
        st.metric("水位", f"{score}%")
        
        if st.button(f"🪨 投石 (G{i})", key=f"add_{i}"):
            st.session_state.scores[i] = min(100, score + 10)
            play_short_sound("stone")
            if st.session_state.scores[i] >= 100:
                play_short_sound("win")
                st.balloons()
            st.rerun()

st.markdown("---")

# --- 联动盲盒逻辑 ---
st.header("🎁 策略盲盒")
# 道具池：(名称, 描述, 对水位的影响值)
prizes = [
    ("🌊 涌泉", "本组 +15%", 15),
    ("🌪️ 狂风", "其他组各 -5%", -5),
    ("🧊 冰封", "指定对手 -10%", -10),
    ("💎 巨石", "本组 +25%", 25),
    ("💧 漏水", "本组 -10%", -10),
    ("🔄 逆转", "与第一名交换水位", 0)
]

box_cols = st.columns(4)
for i in range(8):
    with box_cols[i % 4]:
        if st.button(f"📦 盲盒 {i+1}", key=f"box_{i}"):
            play_short_sound("box")
            name, desc, val = random.choice(prizes)
            st.session_state.log = f"抽取结果：【{name}】 {desc}"
            # 此处建议老师根据抽奖结果，手动点击上方对应组的“投石”或记录分值
            # 这样互动感最强，也防止程序自动扣分引起学生不满
            st.warning(f"结果：{name}!")
            st.write(desc)