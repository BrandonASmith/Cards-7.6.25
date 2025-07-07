import streamlit as st
import matplotlib.pyplot as plt

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

# Betting suggestion logic
def get_bet_advice(tc):
    if tc <= 0:
        return "🧊 Chill Out"
    elif 0 < tc < 1.5:
        return "🧃 More Juice"
    else:
        return "🔥 Foot on the Gas"

# Page style
st.set_page_config(page_title="Hi-Lo Counter", layout="centered")
st.markdown("""
    <style>
    .stButton > button {
        height: 70px;
        width: 70px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid black;
        background-color: white;
        color: black;
    }
    .card-history {
        display: inline-block;
        padding: 8px 14px;
        margin: 4px;
        font-size: 20px;
        font-weight: bold;
        background: white;
        border: 2px solid black;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🃏 Hi-Lo Blackjack Counter")

# Deck count
num_decks = st.selectbox("Number of decks:", range(1, 9), index=5)

# Initialize state
if "count" not in st.session_state or st.session_state.get("num_decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.num_decks = num_decks
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []

# Reset buttons
col1, col2 = st.columns(2)
if col1.button("🔄 Reset Shoe"):
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []

if col2.button("♻️ Reset Hand"):
    st.session_state.dealt = []
    st.session_state.history = []

# Count and advice
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
bet_advice = get_bet_advice(true_count)

st.subheader(f"Running Count: {st.session_state.count}")
st.subheader(f"True Count: {true_count}")
st.subheader(f"Bet Suggestion: {bet_advice}")

# 13 Card Buttons
st.markdown("### Tap a Card to Deal:")
cols = st.columns(len(cards))
for i, card in enumerate(cards):
    remaining = st.session_state.card_counts[card]
    if cols[i].button(f"{card}\n({remaining})", key=f"{card}_btn"):
        if remaining > 0:
            st.session_state.card_counts[card] -= 1
            st.session_state.total_cards -= 1
            st.session_state.count += hi_lo_values[card]
            st.session_state.dealt.append(card)
            st.session_state.history.append(st.session_state.count)

# Dealt history
if st.session_state.dealt:
    st.markdown("### Dealt Cards:")
    dealt_html = ''.join([f"<span class='card-history'>{card}</span>" for card in st.session_state.dealt])
    st.markdown(dealt_html, unsafe_allow_html=True)

# Graph
if st.session_state.history:
    st.markdown("### Running Count History:")
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards Dealt")
    ax.set_ylabel("Running Count")
    ax.set_title("")
    st.pyplot(fig)
