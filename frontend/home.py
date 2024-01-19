import streamlit as st
from k1 import main as k1


# Use a selectbox to let the user choose the view
selected_view = st.sidebar.selectbox("Select View", ["Page 1", "Page 2"])

def main():
    if selected_view == "Page 1":
        k1()
    elif selected_view == "Page 2":
        pass

if __name__ == "__main__":
    main()
