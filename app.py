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
        return "🧊 Chill"
    elif 0 < tc < 1.8:
        return "🧃 More Juice"
    else:
        return "🍊 Fresh Squeezed"

# Page config
st.set_page_config(page_title="JuiceBox", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #163420;
    }
    html, body, [class*="css"] {
        font-size: 14px;
        color: white;
    }
    .stButton>button {
        font-size: 13px !important;
        padding: 6px 8px !important;
        height: 42px !important;
        width: 50px !important;
        margin: 2px !important;
        border-radius: 5px;
    }
    .stSelectbox, .stSelectbox>div {
        font-size: 14px !important;
    }
    .dealt-card {
        display: inline-block;
        font-size: 12px;
        padding: 5px 7px;
        margin: 2px;
        background: white;
        color: black;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h4 style='margin-bottom:2px; color:white;'>Juice 🧃 Box</h4>", unsafe_allow_html=True)

# Dropdown
num_decks = st.selectbox("Number of decks:", range(1, 9), index=5)

# Session state
if "count" not in st.session_state or st.session_state.get("decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.decks = num_decks

# Reset buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔁 Shoe"):
        st.session_state.count = 0
        st.session_state.total_cards = num_decks * 52
        st.session_state.card_counts = {card: num_decks * 4 for card in cards}
        st.session_state.dealt = []
        st.session_state.history = []

with col2:
    if st.button("♻️ Hand"):
        st.session_state.dealt = []

# Counts and suggestion
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
bet = get_bet_advice(true_count)
st.markdown(f"<p><strong>RC:</strong> {st.session_state.count} &nbsp;&nbsp; <strong>TC:</strong> {true_count} &nbsp;&nbsp; {bet}</p>", unsafe_allow_html=True)

# Two rows of card buttons
st.markdown("**Tap a Card to Deal:**", unsafe_allow_html=True)
row1, row2 = st.columns(7)
for i, card in enumerate(cards):
    remaining = st.session_state.card_counts[card]
    col = row1 if i < 7 else row2
    if col.button(f"{card} ({remaining})", key=f"btn_{card}"):
        if remaining > 0:
            st.session_state.count += hi_lo_values[card]
            st.session_state.total_cards -= 1
            st.session_state.card_counts[card] -= 1
            st.session_state.dealt.append(card)
            st.session_state.history.append(st.session_state.count)

# Dealt cards
if st.session_state.dealt:
    st.markdown("**Dealt:**", unsafe_allow_html=True)
    dealt_html = "".join([f"<span class='dealt-card'>♥{card}</span>" for card in st.session_state.dealt])
    st.markdown(dealt_html, unsafe_allow_html=True)

# Optional graph (in expander)
if st.session_state.history:
    with st.expander("📈 Count Graph"):
        fig, ax = plt.subplots(figsize=(4, 1.6))
        ax.plot(st.session_state.history, marker='o', linewidth=1.2)
        ax.set_xticks([])
        ax.set_yticks([])
        st.pyplot(fig)
