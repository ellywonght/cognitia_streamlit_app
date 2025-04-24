import streamlit as st
import time
import random
from datetime import datetime

# Optional: For audio recording
try:
    from audiorecorder import audiorecorder
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

st.set_page_config(page_title="Cognitia - Alzheimer's Early Detection", layout="centered")

# Session state init
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'completed' not in st.session_state:
    st.session_state.completed = {'speech': False, 'reaction': False, 'eye': False, 'pupil': False}

# Helper
def all_done():
    return all(st.session_state.completed.values())

# Screens
def welcome():
    st.title("🧠 Cognitia")
    st.write("**Early Detection of Alzheimer's Disease**")
    st.write("Cognitia uses AI to analyze multiple biomarkers for early detection of Alzheimer's Disease, helping with timely intervention.")
    if st.button("Start Assessment", use_container_width=True):
        st.session_state.page = 'menu'

def menu():
    st.header("📋 Assessment Menu")
    st.write("Please complete all 4 assessments:")
    cols = st.columns(2)
    tests = [
        ('speech','🗣️ Speech & Language'),
        ('reaction','⚡ Reaction Time'),
        ('eye','👁️ Eye Movements'),
        ('pupil','🔆 Pupillary Response')
    ]
    for i,(key,label) in enumerate(tests):
        col = cols[i%2]
        text = f"{label} ✅" if st.session_state.completed[key] else label
        if col.button(text, key=key):
            st.session_state.page = key
    if all_done():
        if st.button("View Results", use_container_width=True):
            st.session_state.page = 'results'
    else:
        st.write("*Complete all tests to view results.*")

def speech_test():
    st.subheader("🗣️ Speech & Language Test")
    st.write("Describe what you did yesterday. Press Start to record 10 seconds of audio.")
    if AUDIO_AVAILABLE:
        audio = audiorecorder("Start Recording", "Stop Recording")
        if len(audio) > 0:
            st.audio(audio.tobytes())
            st.success("Recording saved")
            st.session_state.completed['speech'] = True
    else:
        if st.button("Start Recording (simulated)"):
            time.sleep(2)
            st.success("Recording complete (simulated)")
            st.session_state.completed['speech'] = True
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

def reaction_test():
    st.subheader("⚡ Reaction Time Test")
    st.write("Click the button as soon as it appears. 5 trials.")
    if 'rt_started' not in st.session_state:
        st.session_state.rt_started = False
    if not st.session_state.rt_started:
        if st.button("Start Test"):
            st.session_state.rt_started = True
            st.session_state.rt_times = []
            st.session_state.rt_count = 0
    else:
        placeholder = st.empty()
        delay = random.uniform(1,3)
        time.sleep(delay)
        start = datetime.now()
        if placeholder.button("Tap Now!"):
            elapsed = (datetime.now()-start).total_seconds()*1000
            st.session_state.rt_times.append(elapsed)
            st.session_state.rt_count += 1
            placeholder.empty()
            if st.session_state.rt_count >=5:
                avg = sum(st.session_state.rt_times)/len(st.session_state.rt_times)
                st.success(f"Average reaction time: {avg:.0f} ms")
                st.session_state.completed['reaction'] = True
                del st.session_state.rt_started
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

def eye_test():
    st.subheader("👁️ Eye Movement Test")
    st.write("Use your webcam to capture 3 snapshots during saccadic targets.")
    img1 = st.camera_input("Capture center", key='c1')
    img2 = st.camera_input("Capture left", key='c2')
    img3 = st.camera_input("Capture right", key='c3')
    if img1 and img2 and img3:
        st.success("Shots captured")
        st.session_state.completed['eye'] = True
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

def pupil_test():
    st.subheader("🔆 Pupillary Response Test")
    st.write("Look at the circle: it will simulate light change.")
    box = st.empty()
    if st.button("Start Test"):
        for color in ['black','white','black']:
            box.markdown(f"<div style='width:200px;height:200px;background:{color};border-radius:50%;margin:auto'></div>", unsafe_allow_html=True)
            time.sleep(1)
        st.success("Test complete")
        st.session_state.completed['pupil'] = True
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

def results():
    st.header("🧾 Your Assessment Results")
    for key,label in [('speech','Speech & Language'),('reaction','Reaction Time'),('eye','Eye Movements'),('pupil','Pupillary Response')]:
        mark = '✅' if st.session_state.completed[key] else '❌'
        st.write(f"- {label}: {mark}")
    if st.button("Back to Menu"):
        st.session_state.page = 'menu'

# Main
pages = {
    'welcome': welcome,
    'menu': menu,
    'speech': speech_test,
    'reaction': reaction_test,
    'eye': eye_test,
    'pupil': pupil_test,
    'results': results
}
pages[st.session_state.page]()
