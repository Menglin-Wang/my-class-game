import streamlit as st
import random

# 页面配置
st.set_page_config(page_title="智慧课堂：竞技联动版", layout="wide")

# --- 核心音效逻辑 (适配国内网络) ---
def play_sound(action):
    # 使用国内可访问的 CDN 链接或极简提示音
    sound_urls = {
        "stone": "https://www.w3school.com.cn/i/horse.ogg", # 替换为轻促的投石声(示例)
        "win": "https://www.w3school.com.cn/i/song.mp3",   # 替换为获胜欢呼(示例)
        "box": "https://mdn.github.io/learning-area/html/multimedia-and-embedding/video-and-audio-content/viper.mp3"
    }
    
    # 注入 HTML5 播放代码
    # 提示：由于 Chrome/Edge 策略，必须在页面有点击交互后才能播放
    sound_html = f"""
        <audio autoplay name="media">
            <source src="{sound_urls.get(action)}" type="audio/mpeg">
        </audio>
    """
    st.components.v1.html(sound_html, height=0)

# --- 2. 初始化状态 ---
if 'scores' not in st.session_state:
    st.session_state.scores = {i: 0 for i in range(1, 7)}
if 'log' not in st.session_state:
    st.session_state.log = "游戏开始！准备投石！"

# --- 3. 侧边栏：声音开关与控制 ---
with st.sidebar:
    st.title("⚙️ 课堂控制台")
    # 关键：浏览器要求用户必须先点击页面，才能播放声音
    st.warning("📣 请先点击下方‘激活声音’按钮，确保音效生效")
    if st.button("🔔 激活/测试声音"):
        play_sound("box")
        st.success("声音已激活！")
    
    st.divider()
    if st.button("🔄 重置所有数据"):
        st.session_state.scores = {i: 0 for i in range(1, 7)}
        st.session_state.log = "游戏重置"
        st.rerun()

# --- 4. 主界面：乌鸦喝水竞赛 ---
st.title("🦅 乌鸦喝水：全能竞技场")
st.caption(f"📢 实时战报：{st.session_state.log}")

cols = st.columns(6)
for i in range(1, 7):
    with cols[i-1]:
        st.markdown(f"### 第 {i} 组")
        score = st.session_state.scores[i]
        
        # 视觉进度条
        st.progress(score / 100)
        st.metric("当前水位", f"{score}%")
        
        if st.button(f"🪨 投石 (G{i})", key=f"btn_{i}"):
            st.session_state.scores[i] = min(100, score + 10)
            play_sound("stone") # 触发投石声
            if st.session_state.scores[i] >= 100:
                play_sound("win") # 满水声
                st.balloons()
            st.rerun()

st.markdown("---")

# --- 5. 策略盲盒 (联动加减水) ---
st.header("🎁 策略盲盒 (互动联动)")

# 道具逻辑
prizes = [
    ("🌊 涌泉", "本组水位 +15%", 15),
    ("🌪️ 狂风", "全场其他组 -5%", -5),
    ("🧊 冰封", "指定一组 -10%", -10),
    ("💎 巨石", "本组水位 +25%", 25),
    ("💧 漏水", "本组水位 -5%", -5),
    ("🔄 逆转", "与第一名交换水位", 0)
]

box_cols = st.columns(4)
for i in range(8):
    with box_cols[i % 4]:
        if st.button(f"📦 盲盒 {i+1}", key=f"box_{i}"):
            play_sound("box")
            name, desc, val = random.choice(prizes)
            st.session_state.log = f"第 {i+1} 号盒子：{name} ({desc})"
            st.warning(f"{name}!")
            st.write(desc)
            # 老师根据抽奖结果手动微调水位，增加互动的掌控感