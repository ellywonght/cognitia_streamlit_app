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

# Welcome screen
def welcome_screen():
    st.title("🧠 Cognitia")
    st.markdown("**Early Detection of Alzheimer's Disease**")
    st.markdown("Cognitia uses AI to analyze multiple biomarkers for early detection of Alzheimer's Disease, helping with timely intervention.")
    if st.button("Start Assessment", use_container_width=True):
        st.session_state.page = 'menu'
        st.experimental_rerun()

# Menu screen
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

# Additional test screens and logic omitted for brevity

# Utility to switch page
def switch_page(target):
    st.session_state.page = target

# Router
def run_app():
    page = st.session_state.page
    if page == 'welcome':
        welcome_screen()
    elif page == 'menu':
        menu_screen()
    # Add more page routing here...

run_app()
