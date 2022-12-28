import hypothesis.strategies as st
from pycards.cards import Cards

@st.composite
def card_strategy(draw):
    """
    
    """
    return draw(st.sampled_from(sorted(Cards.standard_deck())))

@st.composite
def cards_strategy(draw):
    """
    Hypothesis strategy for cards
    """
    cards = draw(
        st.lists(
            card_strategy(), min_size=1, max_size=100
        )
    )
    return Cards(cards)