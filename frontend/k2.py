import streamlit as st
from streamlit_option_menu import option_menu
from st_keyup import st_keyup

st.set_page_config(layout="wide")

is_worker = True

if (is_worker):
    worker_navbar = option_menu(None, ["", "", "", "", "", ""],
                                icons=['house', 'person-circle', "search", "file-earmark-bar-graph", "book", "bell"],
                                menu_icon="cast", default_index=0, orientation="horizontal")
else:
    user_navbar = option_menu(None, ["", "", "", "", "", ""],
                              icons=['house', 'person-circle', "search", "wallet", "book", "bell"],
                              menu_icon="cast", default_index=0, orientation="horizontal")


col1, col2 = st.columns([2, 5])
with col1:
    _, filter_column, _ = st.columns([1, 7, 1])
    with filter_column:
        st.header("Filter:")
        label_checkbox = st.write("Status")
        checkbox1 = st.checkbox("Available", value=False)
        checkbox2 = st.checkbox("Borrowed", value=False)
        checkbox3 = st.checkbox("Prepared", value=False)
        checkbox4 = st.checkbox("Unavailable", value=False)
        checkbox5 = st.checkbox("Reserved", value=False)
        with_debounce = st_keyup("Author", debounce=500, key="1")
        with_debounce2 = st_keyup("Title", debounce=500, key="2")
        with_debounce3 = st_keyup("Publication Year", debounce=500, key="3")
        with_debounce4 = st_keyup("Publisher", debounce=500, key="4")
        button_apply = st.button("Apply", key="apply-filter")
        st.write("")

with col2:
    pass


st.components.v1.html("""
    <script>
    const matches = parent.document.querySelectorAll("[data-testid='stVerticalBlock']");
    const match = matches[1];
    match.style.background = "#D6CCC2";
    match.style.textAlign = 'center';
    match.style.borderRadius = '10px';
    </script>
    """, height=0, width=0)
