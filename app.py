
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
    col1.button(button_label('eye', '👁️ Eye Movements'), on_click=lambda: st.session_state.update({'page': 'eye'}))
    col2.button(button_label('pupil', '🔆 Pupillary Response'), on_click=lambda: st.session_state.update({'page': 'pupil'}))

    if all_tests_completed():
        if st.button("View Results", use_container_width=True):
            st.session_state.page = 'results'
    else:
        st.write("Complete all 4 assessments to view your results. This app is a screening tool, not a medical diagnosis.")

def speech_test():
    st.subheader("🗣️ Speech & Language Test")
    st.write("Describe your day yesterday...")
    if st.button("Back to Menu"):
        st.session_state.completed_tests['speech'] = True
        st.session_state.page = 'menu'

def reaction_test():
    st.subheader("⚡ Reaction Time Test")
    st.write("Click the button when ready...")
    if st.button("Back to Menu"):
        st.session_state.completed_tests['reaction'] = True
        st.session_state.page = 'menu'

def eye_test():
    st.subheader("👁️ Eye Movement Test")
    st.write("Follow the moving dot...")
    if st.button("Back to Menu"):
        st.session_state.completed_tests['eye'] = True
        st.session_state.page = 'menu'

def pupil_test():
    st.subheader("🔆 Pupillary Response Test")
    st.write("Stare at the circle during light changes.")
    if st.button("Back to Menu"):
        st.session_state.completed_tests['pupil'] = True
        st.session_state.page = 'menu'

def results_screen():
    st.title("🧾 Assessment Results")
    st.success("All assessments completed!")
    for test in ['speech', 'reaction', 'eye', 'pupil']:
        st.markdown(f"- {test.capitalize()}: ✅")
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

def run_app():
    page = st.session_state.page
    if page == 'welcome':
        welcome_screen()
    elif page == 'menu':
        menu_screen()
    elif page == 'speech':
        speech_test()
    elif page == 'reaction':
        reaction_test()
    elif page == 'eye':
        eye_test()
    elif page == 'pupil':
        pupil_test()
    elif page == 'results':
        results_screen()

run_app()
