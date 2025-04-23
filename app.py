import streamlit as st
import time
import random

st.set_page_config(page_title="Cognitia - Alzheimer's Early Detection", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'results' not in st.session_state:
    st.session_state.results = {
        'speech': None,
        'reaction': None,
        'eye': None,
        'pupil': None
    }

# Function to switch page
def switch_page(target):
    st.session_state.page = target

# Welcome Page
if st.session_state.page == 'welcome':
    st.title("🧠 Cognitia")
    st.subheader("Early Detection of Alzheimer's Disease")
    st.markdown("Cognitia uses AI to analyze multiple biomarkers to assist with early screening and timely intervention.")
    if st.button("Start Assessment", use_container_width=True):
        switch_page('menu')

# Menu Page
elif st.session_state.page == 'menu':
    st.title("📋 Assessment Menu")
    st.markdown("Please complete the following tests:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗣️ Speech & Language"):
            switch_page('speech')
        if st.button("🖱️ Reaction Time"):
            switch_page('reaction')
    with col2:
        if st.button("👁️ Eye Movement"):
            switch_page('eye')
        if st.button("🔆 Pupillary Response"):
            switch_page('pupil')
    completed = all(st.session_state.results.values())
    if st.button("📊 View Results", type="primary", disabled=not completed):
        switch_page('results')

# Speech Test
elif st.session_state.page == 'speech':
    st.title("🗣️ Speech & Language Test")
    st.markdown("Please describe what you did yesterday in 3-4 sentences:")
    text = st.text_area("Enter your answer:")
    if st.button("Analyze"):
        if text.strip():
            score = random.randint(60, 90)
            st.session_state.results['speech'] = score
            st.success(f"Coherence score: {score}/100")
            st.button("Back to Menu", on_click=lambda: switch_page('menu'))
        else:
            st.warning("Please enter a response first.")

# Reaction Test
elif st.session_state.page == 'reaction':
    st.title("🖱️ Reaction Time Test")
    st.markdown("Click the button as fast as you can when it turns green")
    if 'reaction_started' not in st.session_state:
        if st.button("Start Test"):
            time.sleep(random.uniform(1.5, 3.5))
            st.session_state.reaction_started = time.time()
            st.success("Click now!")
            if st.button("Click!"):
                rt = time.time() - st.session_state.reaction_started
                score = max(0, 100 - int(rt * 100))
                st.session_state.results['reaction'] = score
                st.success(f"Your reaction time: {rt:.2f} sec → Score: {score}/100")
                del st.session_state.reaction_started
                st.button("Back to Menu", on_click=lambda: switch_page('menu'))
    else:
        st.info("Wait for the button to appear...")

# Eye Movement Test
elif st.session_state.page == 'eye':
    st.title("👁️ Eye Movement Test")
    st.markdown("Simulating saccadic movement analysis...")
    with st.spinner("Analyzing..."):
        time.sleep(2)
    score = random.randint(65, 95)
    st.session_state.results['eye'] = score
    st.success(f"Eye movement latency score: {score}/100")
    st.button("Back to Menu", on_click=lambda: switch_page('menu'))

# Pupillary Response Test
elif st.session_state.page == 'pupil':
    st.title("🔆 Pupillary Response Test")
    st.markdown("Simulating light reflex analysis...")
    with st.spinner("Simulating light pulse..."):
        time.sleep(2)
    score = random.randint(60, 85)
    st.session_state.results['pupil'] = score
    st.success(f"Pupil constriction delay score: {score}/100")
    st.button("Back to Menu", on_click=lambda: switch_page('menu'))

# Results Page
elif st.session_state.page == 'results':
    st.title("📊 Assessment Results")
    total_score = sum(st.session_state.results.values()) // 4
    st.subheader(f"Overall Risk Score: {total_score}/100")

    if total_score >= 75:
        st.success("🟢 Low risk – Maintain healthy lifestyle.")
    elif total_score >= 50:
        st.warning("🟡 Moderate risk – Consider follow-up testing.")
    else:
        st.error("🔴 High risk – Please consult a neurologist.")

    st.markdown("### Breakdown by Test")
    for key, score in st.session_state.results.items():
        st.markdown(f"- **{key.capitalize()}**: {score}/100")

    st.button("Back to Menu", on_click=lambda: switch_page('menu'))
    st.button("Restart Assessment", on_click=lambda: st.session_state.clear())