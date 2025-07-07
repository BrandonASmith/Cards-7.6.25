import streamlit as st
import matplotlib.pyplot as plt

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

def get_bet_advice(tc):
    if tc <= 0:
        return "🧊 Chill"
    elif 0 < tc < 1.8:
        return "🧃 More Juice"
    else:
        return "🍊 Fresh Squeezed"

def render_card_html(card):
    return f"<div class='card-history'>♥<br>{card}</div>"

st.set_page_config(page_title="JuiceBox", layout="centered")

# Mobile-responsive CSS
st.markdown("""
<style>
.stApp { background-color: #0b6623; }
.stButton > button {
    height: 45px !important;
    width: 48px !important;
    font-size: 14px !important;
    font-weight: bold;
    margin: 2px;
    padding: 0;
}
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    max-width: 100%;
}
.card-history {
    display: inline-block;
    width: 48px;
    height: 65px;
    padding: 4px;
    margin: 2px;
    font-size: 14px;
    font-weight: bold;
    background: white;
    border: 2px solid black;
    border-radius: 6px;
    color: red;
    text-align: center;
    font-family: Georgia, serif;
}
h1, h2, h3 {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("## 🧃 JuiceBox")

# Deck count
num_decks = st.selectbox("Decks:", range(1, 9), index=5)

# Session state setup
if "count" not in st.session_state or st.session_state.get("num_decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks

# Reset buttons
col1, col2 = st.columns(2)
if col1.button("🔁 Shoe"):
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []

if col2.button("♻ Hand"):
    st.session_state.dealt = []
    st.session_state.history = []

# Count display
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
st.markdown(f"**Running Count:** `{st.session_state.count}`")
st.markdown(f"**True Count:** `{true_count}`")
st.markdown(f"**Bet:** {get_bet_advice(true_count)}")

# Card buttons
st.markdown("**Tap to Deal:**")
rows = [cards[i:i+4] for i in range(0, len(cards), 4)]
for row in rows:
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
    st.markdown("**Dealt Cards:**")
    html = ''.join([render_card_html(card) for card in st.session_state.dealt])
    st.markdown(f"<div class='card-container'>{html}</div>", unsafe_allow_html=True)

# Count graph
if st.session_state.history:
    st.markdown("### Count History:")
    fig, ax = plt.subplots(figsize=(3.8, 1.3))
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards Dealt")
    ax.set_ylabel("Running Count")
    st.pyplot(fig)
