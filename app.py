import streamlit as st
import random
import time

# --- 設定頁面 ---
st.set_page_config(page_title="超級99乘法挑戰", page_icon="🚀")

# --- 初始化遊戲狀態 (這是網頁版的記憶體) ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 1
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(2, 9)
if 'num2' not in st.session_state:
    st.session_state.num2 = random.randint(2, 9)
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 20

# --- 誇獎與鼓勵詞庫 ---
praise_words = ["太強了吧！🤩", "答對了！你是天才嗎？✨", "速度好快！🚀", "完全正確！💯", "Bingo！太棒了！🎉"]
encouragement_words = ["沒關係，下次一定會對！💪", "差一點點，加油！🔥", "失敗為成功之母！❤️", "別氣餒，我們再來！😊"]

# --- 核心邏輯函數 ---
def check_answer():
    try:
        user_ans = int(st.session_state.user_input)
        correct_ans = st.session_state.num1 * st.session_state.num2
        
        if user_ans == correct_ans:
            st.session_state.score += (100 / st.session_state.total_questions)
            st.session_state.feedback = f"✅ 答對了！{random.choice(praise_words)}"
            if st.session_state.current_q == st.session_state.total_questions:
                st.balloons() # 答對最後一題放氣球
        else:
            st.session_state.feedback = f"❌ 答錯囉！正確答案是 {correct_ans}。{random.choice(encouragement_words)}"
        
        # 準備下一題
        if st.session_state.current_q < st.session_state.total_questions:
            st.session_state.current_q += 1
            st.session_state.num1 = random.randint(2, 9)
            st.session_state.num2 = random.randint(2, 9)
            # 清空輸入框 (透過將 key 綁定到 widget，Streamlit 會自動重置，這裡利用 key 變更的小技巧)
        else:
            st.session_state.game_over = True
            
    except ValueError:
        st.session_state.feedback = "⚠️ 請輸入數字喔！"

def restart_game():
    st.session_state.current_q = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.feedback = ""
    st.session_state.num1 = random.randint(2, 9)
    st.session_state.num2 = random.randint(2, 9)

# --- 介面顯示 ---
st.title("🚀 超級 99 乘法大挑戰")

if not st.session_state.game_over:
    # 顯示進度條
    progress = (st.session_state.current_q - 1) / st.session_state.total_questions
    st.progress(progress)
    st.write(f"第 {st.session_state.current_q} / {st.session_state.total_questions} 題")
    
    # 顯示題目 (大字體)
    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>{st.session_state.num1} × {st.session_state.num2} = ?</h1>", unsafe_allow_html=True)
    
    # 顯示上一題的回饋
    if st.session_state.feedback:
        if "✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)

    # 輸入區域 (使用 form 讓 iPad 可以按 '換行' 或 'Go' 提交)
    with st.form(key='answer_form', clear_on_submit=True):
        st.number_input("請輸入答案：", min_value=0, max_value=1000, step=1, key="user_input")
        submit_button = st.form_submit_button(label='送出答案 ✨')
    
    if submit_button:
        check_answer()
        st.rerun() # 重新整理頁面以顯示新題目

else:
    # --- 遊戲結束畫面 ---
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
        
    st.button("🔄 再玩一次", on_click=restart_game)
