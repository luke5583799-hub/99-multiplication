import streamlit as st
import random
import time

# --- 設定頁面 ---
st.set_page_config(page_title="超級99乘法挑戰", page_icon="🚀")

# 透過 CSS 讓按鈕變大，適合 iPad 點擊
st.markdown("""
<style>
div.stButton > button:first-child {
    height: 3em;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- 初始化遊戲狀態 ---
if 'current_q' not in st.session_state: st.session_state.current_q = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'num1' not in st.session_state: st.session_state.num1 = random.randint(2, 9)
if 'num2' not in st.session_state: st.session_state.num2 = random.randint(2, 9)
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'feedback' not in st.session_state: st.session_state.feedback = ""
if 'user_input_str' not in st.session_state: st.session_state.user_input_str = "" # 用字串存輸入，就不會有預設0的問題
if 'total_questions' not in st.session_state: st.session_state.total_questions = 20

# --- 詞庫 ---
praise_words = ["太強了吧！🤩", "天才！✨", "速度好快！🚀", "完全正確！💯", "Bingo！🎉"]
encouragement_words = ["沒關係，下次對！💪", "差一點點！🔥", "失敗為成功之母！❤️", "別氣餒！😊"]

# --- 按鈕功能函數 ---
def add_digit(digit):
    """將數字加入輸入框"""
    st.session_state.user_input_str += str(digit)

def delete_digit():
    """刪除最後一個數字"""
    st.session_state.user_input_str = st.session_state.user_input_str[:-1]

def clear_input():
    """清除所有輸入"""
    st.session_state.user_input_str = ""

def check_answer():
    """檢查答案"""
    if not st.session_state.user_input_str:
        st.session_state.feedback = "⚠️ 請先輸入數字再送出喔！"
        return

    try:
        user_ans = int(st.session_state.user_input_str)
        correct_ans = st.session_state.num1 * st.session_state.num2
        
        if user_ans == correct_ans:
            st.session_state.score += (100 / st.session_state.total_questions)
            st.session_state.feedback = f"✅ 答對了！{random.choice(praise_words)}"
            if st.session_state.current_q == st.session_state.total_questions:
                st.balloons()
        else:
            st.session_state.feedback = f"❌ 答錯囉！正確答案是 {correct_ans}。{random.choice(encouragement_words)}"
        
        # 準備下一題
        if st.session_state.current_q < st.session_state.total_questions:
            st.session_state.current_q += 1
            st.session_state.num1 = random.randint(2, 9)
            st.session_state.num2 = random.randint(2, 9)
            st.session_state.user_input_str = "" # 清空輸入
        else:
            st.session_state.game_over = True
            
    except ValueError:
        st.session_state.feedback = "⚠️ 請輸入數字喔！"

def restart_game():
    st.session_state.current_q = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.feedback = ""
    st.session_state.user_input_str = ""
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(2, 9)

# --- 畫面顯示 ---
st.title("🚀 超級 99 乘法大挑戰")

if not st.session_state.game_over:
    # 進度條
    progress = (st.session_state.current_q - 1) / st.session_state.total_questions
    st.progress(progress)
    st.write(f"第 {st.session_state.current_q} / {st.session_state.total_questions} 題")
    
    # 顯示題目與目前的輸入 (如果還沒輸入就顯示 ?)
    display_ans = st.session_state.user_input_str if st.session_state.user_input_str else "?"
    st.markdown(
        f"<h1 style='text-align: center; color: #333;'>{st.session_state.num1} × {st.session_state.num2} = <span style='color: #FF4B4B; border-bottom: 2px solid #FF4B4B;'>{display_ans}</span></h1>", 
        unsafe_allow_html=True
    )
    
    # 顯示回饋訊息
    if st.session_state.feedback:
        if "✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
        st.session_state.feedback = "" # 顯示一次後清空，避免卡在畫面上

    st.write("---")
    
    # --- 自製數字鍵盤區 (3欄版面) ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.button("1", on_click=add_digit, args=(1,), use_container_width=True)
        st.button("4", on_click=add_digit, args=(4,), use_container_width=True)
        st.button("7", on_click=add_digit, args=(7,), use_container_width=True)
        st.button("↺ 清除", on_click=clear_input, use_container_width=True) # 清除全部

    with c2:
        st.button("2", on_click=add_digit, args=(2,), use_container_width=True)
        st.button("5", on_click=add_digit, args=(5,), use_container_width=True)
        st.button("8", on_click=add_digit, args=(8,), use_container_width=True)
        st.button("0", on_click=add_digit, args=(0,), use_container_width=True)

    with c3:
        st.button("3", on_click=add_digit, args=(3,), use_container_width=True)
        st.button("6", on_click=add_digit, args=(6,), use_container_width=True)
        st.button("9", on_click=add_digit, args=(9,), use_container_width=True)
        st.button("⬅️ 退格", on_click=delete_digit, use_container_width=True) # 刪除一個字

    # 送出按鈕 (特別大)
    st.write("") # 空一行
    st.button("送出答案 ✨", on_click=check_answer, type="primary", use_container_width=True)

else:
    # --- 結算畫面 ---
    final_score = round(st.session_state.score)
    st.balloons()
    
    st.markdown(f"<h1 style='text-align: center;'>🏆 挑戰結束！</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>你的得分：{final_score} 分</h2>", unsafe_allow_html=True)
    
    if final_score == 100:
        st.success("👑 評價：【傳說中的數學神童】！太不可思議了！今晚吃頓好料的吧！🍔")
    elif final_score >= 80:
        st.info("🥈 評價：【乘法小達人】！非常棒，只差一點點就完美了！")
    elif final_score >= 60:
        st.warning("🥉 評價：【努力的冒險家】！及格囉，多練習幾次一定可以拿滿分！")
    else:
        st.error("🌱 評價：【潛力新星】！沒關係，剛開始練習比較辛苦，再玩一次吧！")
        
    st.button("🔄 再玩一次", on_click=restart_game, use_container_width=True)
