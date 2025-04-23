
import streamlit as st
import time
import random
import speech_recognition as sr

st.set_page_config(page_title="腦友記 Cognitia", layout="centered")

st.title("🧠 腦友記 Cognitia")
st.markdown("專為早期阿茲海默症檢測而設的AI輕應用。請依次完成以下步驟：")

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'risk_score' not in st.session_state:
    st.session_state.risk_score = None

steps = ["語音能力測試（語音輸入）", "反應時間測試", "眼球追蹤模擬", "模擬瞳孔反應", "綜合分析"]

st.header(f"步驟 {st.session_state.step + 1}: {steps[st.session_state.step]}")

# Step 1: Speech Recognition
if st.session_state.step == 0:
    st.subheader("🎤 請講出：你今朝食咗咩早餐？")
    if st.button("開始錄音"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("錄音中，請開始講...")
            audio = recognizer.listen(source, timeout=5)
            st.success("錄音完成，正在辨識...")
        try:
            result = recognizer.recognize_google(audio, language="zh-HK")
            st.write(f"語音辨識結果：{result}")
            st.session_state.step += 1
        except sr.UnknownValueError:
            st.error("無法辨識語音，請再試一次。")

# Step 2: Reaction Time
elif st.session_state.step == 1:
    if 'reaction_start' not in st.session_state:
        if st.button("開始測試"):
            time.sleep(random.uniform(1, 3))
            st.session_state.reaction_start = time.time()
            st.success("請點擊下面按鈕！")
            st.button("點我！", on_click=lambda: st.session_state.update({'reaction_time': time.time() - st.session_state.reaction_start, 'step': st.session_state.step + 1}))
    elif 'reaction_time' in st.session_state:
        st.write(f"您的反應時間：約 {st.session_state.reaction_time:.2f} 秒")

# Step 3: Eye Tracking Simulation
elif st.session_state.step == 2:
    st.info("🧿 模擬眼球追蹤：如在實體版本中，此步驟將會啟動鏡頭分析眼動狀態。\n\n由於雲端環境不支援鏡頭操作，這裡會模擬分析結果：")
    st.success("👁️ 分析結果：偵測到輕微掃視延遲，建議配合其他項目進行整體評估")
    if st.button("下一步"):
        st.session_state.step += 1

# Step 4: PLR Simulation
elif st.session_state.step == 3:
    st.info("🔆 模擬PLR（瞳孔光反應）：假設光源閃爍，模擬收縮延遲分析...")
    st.success("📊 模擬結果：收縮延遲 0.25 秒，屬正常範圍")
    if st.button("完成模擬"):
        st.session_state.step += 1

# Step 5: Final analysis
elif st.session_state.step == 4:
    if st.session_state.risk_score is None:
        st.session_state.risk_score = random.randint(20, 95)

    score = st.session_state.risk_score
    st.subheader(f"🧾 綜合風險分數：{score} / 100")
    if score >= 70:
        st.error("⚠️ 高風險：建議諮詢腦神經科醫生")
    elif score >= 40:
        st.warning("🟡 中度風險：建議1個月內複檢")
    else:
        st.success("🟢 風險較低：建議每年定期測試")

    st.button("重新開始", on_click=lambda: st.session_state.clear())
