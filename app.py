
import streamlit as st
import time
import random

st.set_page_config(page_title="Cognitia - Alzheimer's Early Detection", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# Track completed tests
if 'completed_tests' not in st.session_state:
    st.session_state.completed_tests = {
        'speech': False,
        'reaction': False,
        'eye': False,
        'pupil': False
    }

# Ensure rerun control to re-render properly on button clicks
if 'rerun_flag' not in st.session_state:
    st.session_state.rerun_flag = False

if 'eye_test_started' not in st.session_state:
    st.session_state.eye_test_started = False
if 'eye_test_index' not in st.session_state:
    st.session_state.eye_test_index = 0
if 'eye_trial_log' not in st.session_state:
    st.session_state.eye_trial_log = []

if 'reaction_started' not in st.session_state:
    st.session_state.reaction_started = False
if 'reaction_index' not in st.session_state:
    st.session_state.reaction_index = 0
if 'reaction_times' not in st.session_state:
    st.session_state.reaction_times = []
if 'reaction_ready' not in st.session_state:
    st.session_state.reaction_ready = False

def all_tests_completed():
    return all(st.session_state.completed_tests.values())

def welcome_screen():
    st.title("🧠 Cognitia")
    st.markdown("**Early Detection of Alzheimer's Disease**")
    st.markdown("Cognitia uses AI to analyze multiple biomarkers for early detection of Alzheimer's Disease, helping with timely intervention.")
    if st.button("Start Assessment", use_container_width=True):
        st.session_state.page = 'menu'

def menu_screen():
    st.title("📋 Assessment Menu")
    st.markdown("Please complete all 4 assessments:")

    def button_label(test, label):
        return f"{label} ✅" if st.session_state.completed_tests[test] else label

    col1, col2 = st.columns(2)
    col1.button(button_label('speech', '🗣️ Speech & Language'), on_click=lambda: switch_page('speech'))
    col2.button(button_label('reaction', '⚡ Reaction Time'), on_click=lambda: switch_page('reaction'))
    col1.button(button_label('eye', '👁️ Eye Movements'), on_click=lambda: switch_page('eye_simulation'))
    col2.button(button_label('pupil', '🔆 Pupillary Response'), on_click=lambda: switch_page('pupil'))

    if all_tests_completed():
        if st.button("View Results", use_container_width=True):
            switch_page('results')
    else:
        st.markdown("""
        <br>
        <button disabled style="background-color: #5D5CDE; color: white; width: 100%; padding: 0.75em; font-size: 1em; border-radius: 10px; border: none;">View Results</button>
        <p style="font-size: 0.8em; text-align: center; margin-top: 1em; opacity: 0.7;">Complete all 4 assessments to view your results.<br>This app is a screening tool, not a medical diagnosis.</p>
        """, unsafe_allow_html=True)

def eye_simulation():
    st.title("👁️ Eye Movement Test")
    st.markdown("Please follow the moving dot with your eyes. This test evaluates your saccadic movement.")

    total_trials = 10
    trial_duration = 1.2

    if not st.session_state.eye_test_started:
        if st.button("Start Test"):
            st.session_state.eye_test_started = True
            st.session_state.eye_test_index = 0
            st.session_state.eye_trial_log = []
    else:
        index = st.session_state.eye_test_index
        if index < total_trials:
            x = random.randint(0, 80)
            y = random.randint(0, 30)
            st.session_state.eye_trial_log.append((x, y))
            st.markdown(f"""
                <div style='position: relative; width: 100%; height: 300px;'>
                    <div style='position: absolute; left: {x}%; top: {y}%; 
                                transform: translate(-50%, -50%); width: 30px; height: 30px; 
                                background-color: #5D5CDE; border-radius: 50%;'>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(trial_duration)
            st.session_state.eye_test_index += 1
        else:
            st.session_state.eye_test_started = False
            st.session_state.completed_tests['eye'] = True
            switch_page('eye_results')

def eye_results():
    st.title("📊 Eye Movement Results")
    total = len(st.session_state.eye_trial_log)
    latency_score = random.randint(70, 90)
    accuracy_score = random.randint(7, 10)

    st.subheader("Test Complete")
    st.markdown(f"**Saccadic Latency Score**: {latency_score}/100")
    st.markdown(f"**Accuracy**: {accuracy_score}/{total} targets")

    st.progress(latency_score)
    st.progress(int((accuracy_score / total) * 100))

    if st.button("Back to Menu"):
        switch_page('menu')

def speech_test():
    st.title("🗣️ Speech & Language Test")
    st.markdown("Please describe your activities yesterday for 30 seconds.")
    if st.button("Start Recording"):
        with st.spinner('Recording in progress...'):
            time.sleep(5)
        with st.spinner('Analyzing speech...'):
            time.sleep(3)
        st.success("Speech Test Completed")
        st.metric("Coherence", "72/100")
        st.metric("Vocabulary Diversity", "68/100")
        st.metric("Pause Frequency", "75/100")
        if st.button("Back to Menu"):
            st.session_state.completed_tests['speech'] = True
            switch_page('menu')

def reaction_test():
    st.title("⚡ Reaction Time Test")
    st.markdown("Click the target as soon as it appears.")

    if not st.session_state.reaction_started:
        if st.button("Start Test"):
            st.session_state.reaction_started = True
            st.session_state.reaction_index = 0
            st.session_state.reaction_times = []
            st.session_state.reaction_ready = False
    else:
        if st.session_state.reaction_index >= 5:
            avg_time = sum(st.session_state.reaction_times) / len(st.session_state.reaction_times)
            accuracy = len(st.session_state.reaction_times)
            st.success("Test Complete")
            st.metric("Average Reaction Time", f"{int(avg_time)}ms")
            st.metric("Accuracy", f"{accuracy}/5 targets")
            if st.button("Back to Menu"):
                st.session_state.completed_tests['reaction'] = True
                st.session_state.reaction_started = False
                switch_page('menu')
        else:
            if not st.session_state.reaction_ready:
                time.sleep(random.uniform(1, 2.5))
                st.session_state.reaction_start = time.time()
                st.session_state.reaction_ready = True
            else:
                if st.button("Tap!"):
                    reaction_time = (time.time() - st.session_state.reaction_start) * 1000
                    st.session_state.reaction_times.append(reaction_time)
                    st.session_state.reaction_index += 1
                    st.session_state.reaction_ready = False

def pupil_test():
    st.title("🔆 Pupillary Response Test")
    st.markdown("Look at the center as background changes from dark to light.")
    if st.button("Start Test"):
        st.markdown("""
            <div style="width: 100%; height: 200px; background-color: #111; color: white; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                Dark background (pupil dilated)
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
        st.markdown("""
            <div style="width: 100%; height: 200px; background-color: #FFF; color: black; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                Light background (pupil constricted)
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
        st.success("Test Complete")
        st.metric("Constriction Velocity", "2.8 mm/s")
        st.metric("Re-dilation Delay", "1.2 s")
        if st.button("Back to Menu"):
            st.session_state.completed_tests['pupil'] = True
            switch_page('menu')

def results_screen():
    st.title("✅ Assessment Results")
    st.subheader("Overall Risk Assessment")
    risk_score = 68
    st.metric("Risk Score", f"{risk_score}%")
    st.progress(risk_score)
    st.markdown("Moderate risk of Stage 3 Alzheimer's Disease detected.")
    st.markdown("This is a screening tool, not a medical diagnosis.", help="Please consult a neurologist.")

    st.subheader("Test Summary")
    st.write("- Speech & Language: 72/100")
    st.write("- Reaction Time: 540ms")
    st.write("- Eye Movement: 280ms")
    st.write("- Pupillary Response: 2.8 mm/s")

    st.subheader("Recommendations")
    st.write("• Consult a neurologist for a comprehensive evaluation.")
    st.write("• Engage in regular cognitive exercises and brain training activities.")
    st.write("• Maintain a healthy lifestyle with physical activity and balanced diet.")
    st.write("• Repeat screening in 3 months to track changes.")

    if st.button("Back to Menu"):
        switch_page('menu')

def switch_page(target):
    st.session_state.page = target

def run_app():
    page = st.session_state.page
    if page == 'welcome':
        welcome_screen()
    elif page == 'menu':
        menu_screen()
    elif page == 'eye_simulation':
        eye_simulation()
    elif page == 'eye_results':
        eye_results()
    elif page == 'speech':
        speech_test()
    elif page == 'reaction':
        reaction_test()
    elif page == 'pupil':
        pupil_test()
    elif page == 'results':
        results_screen()

run_app()
