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

# Eye Movement Test state
if 'eye_test_started' not in st.session_state:
    st.session_state.eye_test_started = False
if 'eye_test_index' not in st.session_state:
    st.session_state.eye_test_index = 0
if 'eye_trial_log' not in st.session_state:
    st.session_state.eye_trial_log = []

# Reaction Test state
if 'reaction_started' not in st.session_state:
    st.session_state.reaction_started = False
if 'reaction_index' not in st.session_state:
    st.session_state.reaction_index = 0
if 'reaction_times' not in st.session_state:
    st.session_state.reaction_times = []
if 'reaction_ready' not in st.session_state:
    st.session_state.reaction_ready = False
if 'reaction_show_target' not in st.session_state:
    st.session_state.reaction_show_target = False
if 'reaction_start_time' not in st.session_state:
    st.session_state.reaction_start_time = 0

# Pupil Test state
if 'pupil_started' not in st.session_state:
    st.session_state.pupil_started = False
if 'pupil_phase' not in st.session_state:
    st.session_state.pupil_phase = 'dark'

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
    col1.button(button_label('speech', '🗣️ Speech & Language'), on_click=lambda: st.session_state.update({'page': 'speech'}))
    col2.button(button_label('reaction', '⚡ Reaction Time'), on_click=lambda: st.session_state.update({'page': 'reaction'}))
    col1.button(button_label('eye', '👁️ Eye Movements'), on_click=lambda: st.session_state.update({'page': 'eye_simulation'}))
    col2.button(button_label('pupil', '🔆 Pupillary Response'), on_click=lambda: st.session_state.update({'page': 'pupil'}))

    if all_tests_completed():
        if st.button("View Results", use_container_width=True):
            st.session_state.page = 'results'
    else:
        st.markdown("""
        <br>
        <button disabled style="background-color: #5D5CDE; color: white; width: 100%; padding: 0.75em; font-size: 1em; border-radius: 10px; border: none;">View Results</button>
        <p style="font-size: 0.8em; text-align: center; margin-top: 1em; opacity: 0.7;">Complete all 4 assessments to view your results.<br>This app is a screening tool, not a medical diagnosis.</p>
        """, unsafe_allow_html=True)

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

# Stub screens for other functions

def eye_simulation():
    st.write("Eye Simulation Placeholder")
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

def eye_results():
    st.write("Eye Results Placeholder")
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

def speech_test():
    st.write("Speech Test Placeholder")
    if st.button("Back to Menu"):
        st.session_state.completed_tests['speech'] = True
        st.session_state.page = 'menu'

def reaction_test():
    st.write("Reaction Test Placeholder")
    if st.button("Back to Menu"):
        st.session_state.completed_tests['reaction'] = True
        st.session_state.page = 'menu'

def pupil_test():
    st.write("Pupil Test Placeholder")
    if st.button("Back to Menu"):
        st.session_state.completed_tests['pupil'] = True
        st.session_state.page = 'menu'

def results_screen():
    st.title("🧾 Your Assessment Results")
    st.markdown("All assessments completed. Here are your results:")
    st.markdown("- Speech & Language: ✅
- Reaction Time: ✅
- Eye Movements: ✅
- Pupillary Response: ✅")
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

run_app()
