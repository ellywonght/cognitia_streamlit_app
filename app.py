import streamlit as st
import time
import random
import plotly.graph_objects as go

# Initialize session state for navigation and test status
if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'
if 'test_status' not in st.session_state:
    st.session_state.test_status = {
        'speech': False,
        'reaction': False,
        'eye': False,
        'pupil': False
    }
if 'speech_results' not in st.session_state:
    st.session_state.speech_results = None
if 'reaction_results' not in st.session_state:
    st.session_state.reaction_results = None
if 'eye_results' not in st.session_state:
    st.session_state.eye_results = None
if 'pupil_results' not in st.session_state:
    st.session_state.pupil_results = None

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        font-family: 'Inter', sans-serif;
    }
    .title {
        color: #5D5CDE;
        font-size: 2em;
        font-weight: bold;
        text-align: center;
    }
    .subtitle {
        color: #1F2937;
        font-size: 1.2em;
        text-align: center;
    }
    .button {
        background-color: #5D5CDE;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
        display: block;
        margin: 10px auto;
    }
    .button:hover {
        background-color: #6366F1;
    }
    .card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .progress-bar {
        width: 100%;
        background-color: #E5E7EB;
        border-radius: 5px;
        height: 10px;
        overflow: hidden;
    }
    .progress-fill {
        background-color: #5D5CDE;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def show_welcome_screen():
    st.markdown('<div class="title">Cognitia</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Early Detection of Alzheimer\'s Disease</div>', unsafe_allow_html=True)
    st.image("https://via.placeholder.com/192x192.png?text=Brain+Icon", width=192)
    st.write("Cognitia uses AI to analyze multiple biomarkers for early detection of Alzheimer's Disease, helping with timely intervention.")
    if st.button("Start Assessment", key="start"):
        st.session_state.screen = 'menu'
    st.markdown('<p style="text-align: center; opacity: 0.7;">A screening tool, not a diagnostic device<br>© 2023 Cognitia Team</p>', unsafe_allow_html=True)

def show_menu_screen():
    st.markdown('<div class="title">Cognitia</div>', unsafe_allow_html=True)
    if st.button("ℹ️ Info", key="info"):
        st.session_state.screen = 'info_modal'
    
    st.write("Please complete all 4 assessments:")
    
    tests = [
        ("speech", "Speech & Language", "Analyze speech patterns and coherence"),
        ("reaction", "Reaction Time & Tasks", "Measure response time and accuracy"),
        ("eye", "Saccadic Eye Movements", "Track eye movement patterns"),
        ("pupil", "Pupillary Light Response", "Measure pupil dilation and constriction")
    ]
    
    for test_id, title, desc in tests:
        status = "Completed" if st.session_state.test_status[test_id] else "Pending"
        status_color = "green" if st.session_state.test_status[test_id] else "gray"
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<div class="card"><h3>{title}</h3><p style="opacity: 0.7;">{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Start {title}", key=f"{test_id}_test"):
                st.session_state.screen = f"{test_id}_test"
        with col2:
            st.markdown(f'<span style="background-color: {status_color}; color: white; padding: 5px 10px; border-radius: 15px;">{status}</span>', unsafe_allow_html=True)
    
    all_completed = all(st.session_state.test_status.values())
    if st.button("View Results", disabled=not all_completed, key="view_results"):
        st.session_state.screen = 'results'
    st.markdown('<p style="opacity: 0.7;">Complete all 4 assessments to view your results.<br>This app is a screening tool, not a medical diagnosis.</p>', unsafe_allow_html=True)

def show_speech_test_screen():
    if st.button("⬅ Back", key="speech_back"):
        st.session_state.screen = 'menu'
    
    st.markdown('<h2>Speech & Language Test</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Instructions:</h3><p>Please answer the following question by speaking clearly for 20-30 seconds. This test analyzes your speech patterns and coherence.</p><div style="background-color: #F3F4F6; padding: 10px; border-radius: 10px;"><p><b>Question:</b></p><p>Please describe what you did yesterday, from morning until evening, with as much detail as you can remember.</p></div></div>', unsafe_allow_html=True)
    
    if 'speech_recording' not in st.session_state:
        st.session_state.speech_recording = False
    if 'speech_analyzing' not in st.session_state:
        st.session_state.speech_analyzing = False
    
    if not st.session_state.speech_recording and not st.session_state.speech_analyzing and not st.session_state.speech_results:
        if st.button("Start Recording", key="start_recording"):
            st.session_state.speech_recording = True
            st.session_state.start_time = time.time()
    
    if st.session_state.speech_recording:
        st.markdown('<div style="text-align: center;"><p>Recording in progress...</p></div>', unsafe_allow_html=True)
        elapsed = time.time() - st.session_state.start_time
        progress = min(elapsed / 5.0, 1.0)  # Simulate 5 seconds
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progress*100}%"></div></div>', unsafe_allow_html=True)
        if elapsed >= 5:
            st.session_state.speech_recording = False
            st.session_state.speech_analyzing = True
    
    if st.session_state.speech_analyzing:
        st.markdown('<div style="text-align: center;"><p>Analyzing speech patterns...</p><p style="opacity: 0.7;">This may take a moment</p></div>', unsafe_allow_html=True)
        time.sleep(3)  # Simulate analysis
        st.session_state.speech_analyzing = False
        st.session_state.speech_results = {
            'coherence': 72,
            'vocabulary': 68,
            'pause': 75
        }
    
    if st.session_state.speech_results:
        st.markdown('<div class="card"><h3 style="text-align: center;">Speech Analysis Results</h3></div>', unsafe_allow_html=True)
        for label, score in [("Coherence score", "coherence"), ("Vocabulary diversity", "vocabulary"), ("Pause frequency", "pause")]:
            value = st.session_state.speech_results[score]
            st.write(f"{label}: {value}/100")
            st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {value}%"></div></div>', unsafe_allow_html=True)
        if st.button("Complete Test", key="speech_complete"):
            st.session_state.test_status['speech'] = True
            st.session_state.speech_results = None
            st.session_state.screen = 'menu'

def show_reaction_test_screen():
    if st.button("⬅ Back", key="reaction_back"):
        st.session_state.screen = 'menu'
    
    st.markdown('<h2>Reaction Time Test</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Instructions:</h3><p>This test measures your reaction time and motor skills.</p><p>Click the button as quickly as possible when it appears. You\'ll need to complete 5 tries.</p></div>', unsafe_allow_html=True)
    
    if 'reaction_trial' not in st.session_state:
        st.session_state.reaction_trial = 0
    if 'reaction_times' not in st.session_state:
        st.session_state.reaction_times = []
    
    max_trials = 5
    if st.session_state.reaction_trial == 0:
        if st.button("Start Test", key="reaction_start"):
            st.session_state.reaction_trial = 1
    
    if 1 <= st.session_state.reaction_trial <= max_trials:
        st.write(f"Trial: {st.session_state.reaction_trial}/{max_trials}")
        if st.button("Tap!", key=f"reaction_tap_{st.session_state.reaction_trial}"):
            reaction_time = random.randint(400, 600)  # Simulate reaction time
            st.session_state.reaction_times.append(reaction_time)
            st.session_state.reaction_trial += 1
            if st.session_state.reaction_trial > max_trials:
                avg_time = sum(st.session_state.reaction_times) // len(st.session_state.reaction_times)
                accuracy = random.randint(4, 5)
                st.session_state.reaction_results = {
                    'avg_time': avg_time,
                    'accuracy': accuracy,
                    'score': max(0, min(100, 100 - (avg_time - 200) // 5))
                }
    
    if st.session_state.reaction_results:
        st.markdown('<div class="card"><h3 style="text-align: center;">Reaction Test Results</h3></div>', unsafe_allow_html=True)
        st.write(f"Average reaction time: {st.session_state.reaction_results['avg_time']}ms")
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {st.session_state.reaction_results['score']}%"></div></div>', unsafe_allow_html=True)
        st.write(f"Accuracy: {st.session_state.reaction_results['accuracy']}/5 targets")
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {st.session_state.reaction_results['accuracy']*20}%"></div></div>', unsafe_allow_html=True)
        st.write("Healthy baseline: 200-300ms")
        if st.button("Complete Test", key="reaction_complete"):
            st.session_state.test_status['reaction'] = True
            st.session_state.reaction_results = None
            st.session_state.reaction_trial = 0
            st.session_state.reaction_times = []
            st.session_state.screen = 'menu'

def show_eye_test_screen():
    if st.button("⬅ Back", key="eye_back"):
        st.session_state.screen = 'menu'
    
    st.markdown('<h2>Eye Movement Test</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Instructions:</h3><p>This test analyzes your saccadic eye movements.</p><p>Click the button to simulate following a moving dot. Complete 10 trials.</p></div>', unsafe_allow_html=True)
    
    if 'eye_trial' not in st.session_state:
        st.session_state.eye_trial = 0
    
    max_trials = 10
    if st.session_state.eye_trial == 0:
        if st.button("Start Test", key="eye_start"):
            st.session_state.eye_trial = 1
    
    if 1 <= st.session_state.eye_trial <= max_trials:
        st.write(f"Trial: {st.session_state.eye_trial}/{max_trials}")
        if st.button("Follow Dot", key=f"eye_tap_{st.session_state.eye_trial}"):
            st.session_state.eye_trial += 1
            if st.session_state.eye_trial > max_trials:
                latency = random.randint(250, 300)
                accuracy = random.randint(7, 9)
                st.session_state.eye_results = {
                    'latency': latency,
                    'accuracy': accuracy,
                    'score': max(0, min(100, 100 - (latency - 200) * 0.5))
                }
    
    if st.session_state.eye_results:
        st.markdown('<div class="card"><h3 style="text-align: center;">Eye Movement Results</h3></div>', unsafe_allow_html=True)
        st.write(f"Saccadic latency: {st.session_state.eye_results['latency']}ms")
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {st.session_state.eye_results['score']}%"></div></div>', unsafe_allow_html=True)
        st.write(f"Accuracy: {st.session_state.eye_results['accuracy']}/10 targets")
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {st.session_state.eye_results['accuracy']*10}%"></div></div>', unsafe_allow_html=True)
        st.write("Healthy baseline: 200-250ms")
        if st.button("Complete Test", key="eye_complete"):
            st.session_state.test_status['eye'] = True
            st.session_state.eye_results = None
            st.session_state.eye_trial = 0
            st.session_state.screen = 'menu'

def show_pupil_test_screen():
    if st.button("⬅ Back", key="pupil_back"):
        st.session_state.screen = 'menu'
    
    st.markdown('<h2>Pupillary Response Test</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card"><h3>Instructions:</h3><p>This test measures your pupil\'s response to light changes.</p><p>Click the button to simulate a light change. Try not to blink during the test.</p></div>', unsafe_allow_html=True)
    
    if 'pupil_running' not in st.session_state:
        st.session_state.pupil_running = False
    
    if not st.session_state.pupil_running and not st.session_state.pupil_results:
        if st.button("Start Test", key="pupil_start"):
            st.session_state.pupil_running = True
            st.session_state.pupil_start_time = time.time()
    
    if st.session_state.pupil_running:
        st.markdown('<div style="text-align: center;"><p>Keep looking at the center</p></div>', unsafe_allow_html=True)
        elapsed = time.time() - st.session_state.pupil_start_time
        if elapsed < 2:
            st.markdown('<div style="width: 128px; height: 128px; border: 4px solid gray; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto;"><div style="width: 20px; height: 20px; background-color: black; border-radius: 50%;"></div></div>', unsafe_allow_html=True)
        elif elapsed < 5:
            st.markdown('<div style="width: 128px; height: 128px; border: 4px solid gray; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: auto;"><div style="width: 8px; height: 8px; background-color: black; border-radius: 50%;"></div></div>', unsafe_allow_html=True)
        if elapsed >= 5:
            st.session_state.pupil_running = False
            st.session_state.pupil_results = {
                'constriction': 2.8,
                'redilation': 1.2,
                'score': 70
            }
    
    if st.session_state.pupil_results:
        st.markdown('<div class="card"><h3 style="text-align: center;">Pupillary Response Results</h3></div>', unsafe_allow_html=True)
        st.write(f"Constriction velocity: {st.session_state.pupil_results['constriction']}mm/s")
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {st.session_state.pupil_results['score']}%"></div></div>', unsafe_allow_html=True)
        st.write(f"Re-dilation delay: {st.session_state.pupil_results['redilation']}s")
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: 65%"></div></div>', unsafe_allow_html=True)
        st.write("Healthy baseline: 3.0-4.0mm/s")
        if st.button("Complete Test", key="pupil_complete"):
            st.session_state.test_status['pupil'] = True
            st.session_state.pupil_results = None
            st.session_state.pupil_running = False
            st.session_state.screen = 'menu'

def show_results_screen():
    if st.button("⬅ Back", key="results_back"):
        st.session_state.screen = 'menu'
    
    st.markdown('<h2>Assessment Results</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="card"><h3>Overall Risk Assessment</h3><p style="font-size: 1.5em; color: #5D5CDE; font-weight: bold; text-align: right;">68%</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="progress-bar"><div class="progress-fill" style="width: 68%"></div></div>', unsafe_allow_html=True)
    st.write("Moderate risk of Stage 3 Alzheimer's Disease detected.")
    st.markdown('<p style="color: red; font-weight: bold;">This is a screening tool, not a diagnosis. Consult a neurologist.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="card"><h3>Test Results Summary</h3></div>', unsafe_allow_html=True)
    results = [
        ("Speech & Language", "72/100", 72),
        ("Reaction Time", "540ms", 65),
        ("Eye Movements", "280ms", 70),
        ("Pupillary Response", "2.8mm/s", 70)
    ]
    for title, value, width in results:
        st.write(f"{title}: {value}")
        st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {width}%"></div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card"><h3>Recommendations</h3><ul><li>Consult with a neurologist for a comprehensive evaluation.</li><li>Engage in regular cognitive exercises and brain training activities.</li><li>Maintain a healthy lifestyle with regular physical activity and a balanced diet.</li><li>Repeat this screening in 3 months to track any changes in cognitive function.</li></ul></div>', unsafe_allow_html=True)
    
    if st.button("Share Results with Doctor", key="share_results"):
        st.session_state.screen = 'share_modal'
    
    st.markdown('<p style="text-align: center; opacity: 0.7;">This is a screening tool only. Results should be reviewed by a healthcare professional.</p>', unsafe_allow_html=True)

def show_info_modal():
    st.markdown('<div class="card"><h3>About Cognitia</h3><p>Cognitia is a mobile application designed for early detection of Alzheimer\'s Disease (AD).</p><p>The app uses AI learning models to analyze multiple biomarkers, such as:</p><ul style="list-style-type: disc; padding-left: 20px;"><li>Speech and language patterns</li><li>Reaction time and motor skills</li><li>Saccadic eye movements</li><li>Pupillary light response</li></ul><p>By comparing these measurements to healthy baselines, Cognitia provides a comprehensive risk assessment for different AD stages.</p><p style="color: red; font-weight: bold;">Important: This is a screening tool only, not a diagnostic device. Results should be reviewed by a healthcare professional.</p></div>', unsafe_allow_html=True)
    if st.button("Got it", key="close_info"):
        st.session_state.screen = 'menu'

def show_share_modal():
    st.markdown('<div class="card"><h3>Share Results</h3><p>Enter your doctor\'s email to share your assessment results:</p></div>', unsafe_allow_html=True)
    email = st.text_input("Doctor's Email", placeholder="doctor@example.com")
    st.markdown('<div style="background-color: #F3F4F6; padding: 10px; border-radius: 10px;"><p><b>Information to be shared:</b></p><ul style="list-style-type: disc; padding-left: 20px;"><li>Test scores and metrics</li><li>Risk assessment summary</li><li>Date and time of assessment</li></ul></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Share Results", key="send_results"):
            st.write("Results have been shared with your doctor.")
            st.session_state.screen = 'results'
    with col2:
        if st.button("Cancel", key="cancel_share"):
            st.session_state.screen = 'results'

# Navigation logic
screens = {
    'welcome': show_welcome_screen,
    'menu': show_menu_screen,
    'speech_test': show_speech_test_screen,
    'reaction_test': show_reaction_test_screen,
    'eye_test': show_eye_test_screen,
    'pupil_test': show_pupil_test_screen,
    'results': show_results_screen,
    'info_modal': show_info_modal,
    'share_modal': show_share_modal
}

screens[st.session_state.screen]()
