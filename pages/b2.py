from random import random

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
if 'is_worker' not in st.session_state:
    st.session_state.is_worker = True

navbar = None


if st.session_state.is_worker:
    navbar = option_menu(None, ["Home", "Account", "Search", "Reports", "Books", "Notifications"],
                                icons=['house', 'person-circle', "search", "file-earmark-bar-graph", "book", "bell"],
                                menu_icon="cast", default_index=3, orientation="horizontal", key='menu_5')
else:
    navbar = option_menu(None, ["Home", "Account", "Search", "Wallet", "Books", "Notifications"],
                              icons=['house', 'person-circle', "search", "wallet", "book", "bell"],
                              menu_icon="cast", default_index=5, orientation="horizontal", key='menu_5')
# Function to generate a random graph
def generate_random_graph():
    plt.xlabel('year')
    plt.ylabel('books number')
    plt.title('Book number over time')
    # x = np.arange(0, 10, 1)
    # change x to display dates
    x = np.arange(2017, 2024, 1)
    y = (np.sin(x) + 300) * 200
    plt.plot(x, y)
    return plt

# Streamlit app
def main():
    st.title('Number of books - report generator')

    # Button to generate a new random graph
    if st.button('Generate book number report'):
        st.pyplot(generate_random_graph())

if __name__ == '__main__':
    main()
