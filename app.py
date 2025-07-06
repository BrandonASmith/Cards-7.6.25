import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os

hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}
        .element-container button {{
            height: 50px !important;
            font-size: 18px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

if os.path.exists("blue_felt.png"):
    set_background("blue_felt.png")

st.title("🃏 Blackjack Hi-Lo Card Counter")

if "count" not in st.session_state:
    st.session_state.count = 0
    st.session_state.history = []
    st.session_state.card_counts = {}
    st.session_state.total_cards = 0

num_decks = st.selectbox("Number of decks:", range(1, 9), index=2)

if not st.session_state.card_counts or st.session_state.total_cards != num_decks * 52:
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.total_cards = num_decks * 52
    st.session_state.count = 0
    st.session_state.history = []

st.subheader(f"Running Count: {st.session_state.count}")
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
st.subheader(f"True Count: {true_count}")

st.markdown("### Deal a card:")
card_rows = [cards[:7], cards[7:]]
for row in card_rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        if cols[i].button(card):
            if st.session_state.card_counts[card] > 0:
                st.session_state.card_counts[card] -= 1
                st.session_state.count += hi_lo_values[card]
                st.session_state.total_cards -= 1
                st.session_state.history.append(st.session_state.count)

st.markdown("### Cards Remaining:")
df = pd.DataFrame({
    "Card": cards,
    "Remaining": [f"{st.session_state.card_counts[c]}/{num_decks * 4}" for c in cards]
})
st.dataframe(df, use_container_width=True)

if st.session_state.history:
    st.markdown("### Count History:")
    fig, ax = plt.subplots()
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards Dealt")
    ax.set_ylabel("Running Count")
    ax.set_title("Running Count Over Time")
    st.pyplot(fig)
