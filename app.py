
import streamlit as st
import time
import random
import base64
from datetime import datetime

st.set_page_config(page_title="腦友記 Cognitia", layout="centered")

st.title("🧠 腦友記 Cognitia")
st.markdown("一個模擬多模態阿茲海默症早期檢測的 Web App。")

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'risk_score' not in st.session_state:
    st.session_state.risk_score = None
if 'session_log' not in st.session_state:
    st.session_state.session_log = []

steps = ["語言能力測試（輸入回答）", "反應時間測試", "眼球追蹤模擬", "模擬瞳孔反應", "綜合分析"]

st.header(f"步驟 {st.session_state.step + 1}: {steps[st.session_state.step]}")

if st.session_state.step == 0:
    st.subheader("📝 請輸入：你今朝食咗咩早餐？")
    user_input = st.text_area("模擬語音辨識輸出（請輸入你想講嘅內容）")
    if st.button("下一步"):
        if user_input.strip() == "":
            st.warning("請輸入內容後再繼續")
        else:
            st.success(f"模擬語音辨識結果：{user_input}")
            st.session_state.session_log.append(f"語言測試輸入：{user_input}")
            st.session_state.step += 1

elif st.session_state.step == 1:
    if 'reaction_start' not in st.session_state:
        if st.button("開始測試"):
            time.sleep(random.uniform(1, 2))
            st.session_state.reaction_start = time.time()
            st.success("請點擊下面按鈕！")
            st.button("點我！", on_click=lambda: st.session_state.update({
                'reaction_time': time.time() - st.session_state.reaction_start,
                'step': st.session_state.step + 1
            }))
    elif 'reaction_time' in st.session_state:
        rt = st.session_state.reaction_time
        st.session_state.session_log.append(f"反應時間：{rt:.2f} 秒")
        st.write(f"您的反應時間：約 {rt:.2f} 秒")

elif st.session_state.step == 2:
    st.info("🧿 模擬眼球追蹤：系統將模擬分析掃視穩定性與跳動頻率")
    st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXd4enhtYnM0andvdWl1dHFhZmVyaWF5M24wMGRpc2xwb2V0cW50dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hxQfpbTIFe42ZpCD7z/giphy.gif", caption="模擬眼動範例", format="GIF")
    st.success("分析結果：掃視速度偏慢，建議配合其他模態綜合分析")
    st.session_state.session_log.append("眼球模擬：掃視速度偏慢")
    if st.button("下一步"):
        st.session_state.step += 1

elif st.session_state.step == 3:
    st.info("🔆 模擬PLR（瞳孔光反應）：假設光源閃爍，系統將分析延遲率")
    st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGt3NDZ1cDBrbjBmbGVma2FydDFueG9odW9tcGphd2UzbTgwNTIxbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/up6guo5ka5gv6/giphy.gif", caption="模擬PLR反應", format="GIF")
    st.success("收縮延遲 0.23 秒，屬正常範圍")
    st.session_state.session_log.append("PLR 模擬：收縮延遲 0.23 秒")
    if st.button("完成模擬"):
        st.session_state.step += 1

elif st.session_state.step == 4:
    if st.session_state.risk_score is None:
        st.session_state.risk_score = random.randint(25, 95)

    score = st.session_state.risk_score
    st.subheader(f"🧾 綜合風險分數：{score} / 100")
    if score >= 70:
        st.error("⚠️ 高風險：建議諮詢腦神經科醫生")
        st.session_state.session_log.append(f"綜合風險分數：{score}（高風險）")
    elif score >= 40:
        st.warning("🟡 中度風險：建議 1 個月內複檢")
        st.session_state.session_log.append(f"綜合風險分數：{score}（中度風險）")
    else:
        st.success("🟢 風險較低：建議每年定期測試")
        st.session_state.session_log.append(f"綜合風險分數：{score}（低風險）")

    if st.button("下載測試報告"):
        report = f"Cognitia 測試報告\n\n時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" + "\n".join(st.session_state.session_log)
        b64 = base64.b64encode(report.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="cognitia_report.txt">📄 點此下載報告</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.button("重新開始", on_click=lambda: st.session_state.clear())
