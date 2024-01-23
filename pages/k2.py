import streamlit as st
from streamlit_option_menu import option_menu
from st_keyup import st_keyup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.database.create_database import Klient, Powiadomienie
from streamlit_modal import Modal

st.set_page_config(layout="wide")

url = 'mysql+pymysql://root:password@localhost:13306/sowa'  # Update with your database connection details
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'is_worker' not in st.session_state:
    st.session_state.is_worker = False

if 'powiadomienia' not in st.session_state:
    st.session_state.powiadomienia = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = 18001

def get_powiadomienia():
    st.session_state.powiadomienia = session.query(Powiadomienie).filter(Powiadomienie.KlientId == st.session_state.user_id).filter(Powiadomienie.Status == False).all()


get_powiadomienia()
navbar = None


if st.session_state.is_worker:
    navbar = option_menu(None, ["Home", "Account", "Search", "Reports", "Books", "Notifications"],
                                icons=['house', 'person-circle', "search", "file-earmark-bar-graph", "book", "bell"],
                                menu_icon="cast", default_index=0, orientation="horizontal", key='menu_5')
else:
    navbar = option_menu(None, ["Home", "Account", "Search", "Wallet", "Books", "Notifications"],
                              icons=['house', 'person-circle', "search", "wallet", "book", "bell"],
                              menu_icon="cast", default_index=5, orientation="horizontal", key='menu_5')


st.title("List of Notifications")

n = 4

page = st.session_state.page if 'page' in st.session_state else 0
active_powiadomienia = st.session_state.powiadomienia[page * n:(page + 1) * n]

for powiadomienie in active_powiadomienia:
    st.markdown(
            f"""
                <div style="background-color: #E3D5CA; padding: 10px; border-radius: 10px;">
                    <h3>{powiadomienie.Tresc}</h3>
                </div>
                """,
            unsafe_allow_html=True
        )
    st.write("---")


prev_page_col, separator, next_page_col = st.columns([1, 4, 1])

if page > 0:
    with prev_page_col:
        if st.button(f"Previous Page ({max(page - 1, 0)})"):
            st.session_state.page = max(0, page - 1)
            st.rerun()
if page < len(st.session_state.powiadomienia) // n - 1:
    with next_page_col:
        if st.button(f"Next Page ({page + 1})"):
            st.session_state.page += 1
            st.rerun()

session.close()
