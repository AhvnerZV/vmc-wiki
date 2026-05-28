"""
app.py
Streamlit frontend for the Volleyball Masterclass Wiki LLM.
Dark court aesthetic: near-black background, volt yellow accent, Barlow Condensed.
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from query import answer

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VMC Wiki | AI Coach",
    page_icon="🏐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800;900&family=Barlow:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: #0A0C0F;
    color: #F0F0F0;
}

h1, h2, h3 {
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 0.04em;
}

.stTextInput > div > div > input {
    background: #12151A;
    border: 1px solid #2A2F3A;
    color: #F0F0F0;
    border-radius: 8px;
    font-family: 'Barlow', sans-serif;
}

.stButton > button {
    background: #FFD100;
    color: #0A0C0F;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.06em;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
}

.stButton > button:hover {
    background: #FFE033;
}

.sidebar .sidebar-content {
    background: #0D1017;
}

.player-card {
    background: #12151A;
    border: 1px solid #1E2530;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 13px;
}

.position-tag {
    display: inline-block;
    background: #FFD100;
    color: #0A0C0F;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.08em;
    padding: 2px 7px;
    border-radius: 4px;
    margin-left: 8px;
}

.user-msg {
    background: #FFD100;
    color: #0A0C0F;
    padding: 12px 16px;
    border-radius: 12px 12px 2px 12px;
    margin: 8px 0 8px 20%;
    font-size: 15px;
    font-weight: 500;
}

.ai-msg {
    background: #12151A;
    border: 1px solid #1E2530;
    padding: 14px 18px;
    border-radius: 12px 12px 12px 2px;
    margin: 8px 20% 8px 0;
    font-size: 15px;
    line-height: 1.6;
}

.source-tag {
    display: inline-block;
    background: #1A2030;
    border: 1px solid #2A3040;
    color: #8899AA;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 20px;
    margin: 6px 4px 0 0;
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 0.04em;
}

.stat-block {
    text-align: center;
    padding: 12px;
}

.stat-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #FFD100;
}

.stat-label {
    font-size: 11px;
    color: #8899AA;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <h2 style="font-family:'Barlow Condensed',sans-serif;font-size:22px;
    letter-spacing:0.06em;color:#FFD100;margin-bottom:4px;">
    VMC WIKI
    </h2>
    <p style="font-size:12px;color:#8899AA;margin-top:0;">AI Coaching Assistant</p>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**ROSTER**", unsafe_allow_html=True)

    players = [
        ("Wilfredo León", "OH"),
        ("Antoine Brizard", "S"),
        ("Jenia Grebennikov", "L"),
        ("TJ DeFalco", "OPP"),
        ("Nimir Abdel-Aziz", "OPP"),
        ("Luciano De Cecco", "S"),
        ("Reid Hall", "COACH"),
    ]

    for name, pos in players:
        st.markdown(f"""
        <div class="player-card">
            {name} <span class="position-tag">{pos}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stat-block"><div class="stat-num">7</div><div class="stat-label">Players</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-block"><div class="stat-num">54+</div><div class="stat-label">Lessons</div></div>', unsafe_allow_html=True)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-family:'Barlow Condensed',sans-serif;font-size:42px;
font-weight:900;letter-spacing:0.04em;margin-bottom:4px;">
ASK THE WORLD'S BEST
</h1>
<p style="color:#8899AA;font-size:15px;margin-top:0;">
Coaching intelligence from elite professional players. Ask anything about volleyball technique,
tactics, or mindset.
</p>
""", unsafe_allow_html=True)

# Example questions
st.markdown("**Try asking:**")
examples = [
    "How does León approach his jump serve?",
    "What's De Cecco's blocking strategy?",
    "How should I reset mentally after an error?",
]
cols = st.columns(3)
for i, ex in enumerate(examples):
    if cols[i].button(ex, key=f"ex_{i}"):
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.history = []
        st.session_state.pending_question = ex

st.divider()

# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.history = []

# Render conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        sources_html = "".join(
            f'<span class="source-tag">{p}</span>'
            for p in msg.get("players", [])
        )
        st.markdown(f"""
        <div class="ai-msg">
            {msg["content"]}
            <br>{sources_html}
        </div>
        """, unsafe_allow_html=True)

# Input
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input(
        "",
        placeholder="Ask about serve technique, blocking, mental performance...",
        label_visibility="collapsed",
        key="input_field"
    )
    submitted = st.form_submit_button("ASK")

# Handle example button injection
if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    submitted = True
    del st.session_state.pending_question

if submitted and question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("Consulting the coaches..."):
        result = answer(question, history=st.session_state.history)
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "players": result["players_cited"]
    })
    st.session_state.history.append({"role": "user", "content": question})
    st.session_state.history.append({"role": "assistant", "content": result["answer"]})
    st.rerun()
