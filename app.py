import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os
import time

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

# Betting logic
def get_betting_suggestion(true_count):
    if true_count <= 0:
        return "💸 Minimum Bet"
    elif 1 <= true_count < 3:
        return "💰 Moderate Bet"
    else:
        return "💵 Maximum Bet"

# Optional background
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        </style>
    """, unsafe_allow_html=True)

# Card styling and app-wide style overrides
st.markdown("""
    <style>
    h1 { font-size: 28px !important; }
    h2, h3, h4, .stSubheader { font-size: 18px !important; }
    .stButton > button {
        height: 70px;
        width: 70px;
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #000;
        background-color: white;
        color: black;
    }
    .dealt-card {
        display: inline-block;
        margin-right: 6px;
        padding: 8px 14px;
        border: 2px solid black;
        background-color: white;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }
    </style>
""", unsafe_allow_html=True)

if os.path.exists("blue_felt.png"):
    set_background("blue_felt.png")

st.title("🃏 Blackjack Hi-Lo Card Counter")

# Deck selection
num_decks = st.selectbox("Number of decks:", range(1, 9), index=5)

# Session setup
if "card_counts" not in st.session_state or st.session_state.get("num_decks", 0) != num_decks:
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.total_cards = num_decks * 52
    st.session_state.count = 0
    st.session_state.history = []
    st.session_state.num_decks = num_decks
    st.session_state.dealt_cards = []

# Reset functions
def reset_shoe():
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.total_cards = num_decks * 52
    st.session_state.count = 0
    st.session_state.history = []
    st.session_state.dealt_cards = []

def reset_hand():
    st.session_state.history = []
    st.session_state.dealt_cards = []

# Reset buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Reset Shoe"):
        reset_shoe()
with col2:
    if st.button("♻️ Reset Hand"):
        reset_hand()

# Running count, true count, betting suggestion
st.markdown(f"<h4>Running Count: {st.session_state.count}</h4>", unsafe_allow_html=True)
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
st.markdown(f"<h4>True Count: {true_count}</h4>", unsafe_allow_html=True)
st.markdown(f"<h4>💡 Betting Suggestion: {get_betting_suggestion(true_count)}</h4>", unsafe_allow_html=True)

# Player hand display with "dealer-style animation"
if st.session_state.dealt_cards:
    st.markdown("### Player Hand:")
    hand_html = ''.join([f"<div class='dealt-card'>{card}</div>" for card in st.session_state.dealt_cards])
    st.markdown(f"<div style='margin-bottom:15px'>{hand_html}</div>", unsafe_allow_html=True)

# Card dealing buttons
st.markdown("<h4>Deal a Card:</h4>", unsafe_allow_html=True)
card_rows = [cards[:7], cards[7:]]
for row in card_rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        remaining = st.session_state.card_counts.get(card, 0)
        if cols[i].button(f"{card}\n({remaining})", key=f"{card}_btn"):
            if remaining > 0:
                st.session_state.card_counts[card] -= 1
                st.session_state.total_cards -= 1
                st.session_state.count += hi_lo_values[card]
                st.session_state.history.append(st.session_state.count)
                st.session_state.dealt_cards.append(card)

# Count graph
if st.session_state.history:
    st.markdown("### Count History:")
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards Dealt")
    ax.set_ylabel("Running Count")
    ax.set_title("")
    st.pyplot(fig)
