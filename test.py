import streamlit as st
from streamlit_modal import Modal

modal = Modal(
    "",
    key="demo-modal",

    # Optional
    padding=20,  # default value
    max_width=300  # default value
)

modal1 = Modal(
    "Jakis tytaaaaaaul",
    key="modal_edit",
    max_width=900
)
open_modal1 = st.button("Start")

if open_modal1:
    modal1.open()

if modal1.is_open():
    with modal1.container():
        col1,col2,col3 = st.columns([1, 8, 1])
        with col2:
            name_input = st.text_input("Title:")
            author_input = st.text_input("Author:")
            publisher_input = st.text_input("Publisher:")
            year_input = st.text_input("Year:")

            col4, col5, col6 = st.columns([1, 7, 1])
            with col4:
                return_button = st.button("Back")

            if return_button:
                modal1.close()

            with col6:
                open_modal = st.button("Save")

            if open_modal:
                modal.open()

            if modal.is_open():
                with modal.container():
                    st.write("Are you sure?")
                    yes = st.button("Yes")