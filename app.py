import streamlit as st
import matplotlib.pyplot as plt

hi_lo_values = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0,
                '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}
cards = list(hi_lo_values.keys())

def get_bet_advice(tc):
    if tc <= 0:
        return "🧊 Chill"
    elif 0 < tc < 1.8:
        return "🧃 More Juice"
    else:
        return "🍊 Fresh Squeezed"

st.set_page_config(page_title="JuiceBox", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0b6623; padding: 0.5rem; }
div[data-testid="column"] { padding: 0 !important; margin: 0 !important; }
button[kind="secondary"] {
    height: 26px !important;
    width: 32px !important;
    font-size: 10px !important;
    padding: 2px !important;
    margin: 1px !important;
}
.stSelectbox label { font-size: 10px !important; margin-bottom: 0px; }
.card-container {
    display: flex; flex-wrap: wrap; gap: 2px; justify-content: center;
}
.card-history {
    display: inline-block;
    width: 28px; height: 38px;
    font-size: 9px; font-weight: bold;
    background: white; border: 1px solid black;
    border-radius: 4px; color: red;
    text-align: center; font-family: Georgia, serif;
    padding: 2px;
}
</style>
""", unsafe_allow_html=True)

# Deck select + buttons in one line
col1, col2, col3 = st.columns([2, 1, 1])
num_decks = col1.selectbox("Decks", range(1, 9), index=5, label_visibility="collapsed")
if col2.button("🔁", help="Reset Shoe"):
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks
if col3.button("♻", help="Reset Hand"):
    st.session_state.dealt = []
    st.session_state.history = []

if "count" not in st.session_state or st.session_state.get("num_decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks

true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
bet = get_bet_advice(true_count)
st.markdown(f"<small><b>RC:</b> {st.session_state.count} &nbsp; <b>TC:</b> {true_count} &nbsp; <b>{bet}</b></small>", unsafe_allow_html=True)

# 13 card buttons in 2 rows
row1 = cards[:7]
row2 = cards[7:]
for row in [row1, row2]:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        rem = st.session_state.card_counts[card]
        if cols[i].button(f"{card}\n({rem})", key=f"{card}_btn"):
            if rem > 0:
                st.session_state.card_counts[card] -= 1
                st.session_state.total_cards -= 1
                st.session_state.count += hi_lo_values[card]
                st.session_state.dealt.append(card)
                st.session_state.history.append(st.session_state.count)

# Dealt cards
if st.session_state.dealt:
    html = ''.join([f"<div class='card-history'>♥<br>{card}</div>" for card in st.session_state.dealt])
    st.markdown(f"<div class='card-container'>{html}</div>", unsafe_allow_html=True)

# Mini graph (optional)
if st.session_state.history:
    fig, ax = plt.subplots(figsize=(2.5, 1))
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards", fontsize=6)
    ax.set_ylabel("RC", fontsize=6)
    ax.tick_params(axis='both', labelsize=6)
    st.pyplot(fig)
