import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.create_database import Klient, Uzytkownik, Autorstwo, Egzemplarz
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

url = 'mysql+pymysql://root:password@localhost:13306/sowa'  # Update with your database connection details
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def get_all_clients():
    return session.query(Klient).all()


def get_user_data(user_id):
    return session.query(Uzytkownik).where(Uzytkownik.Id == user_id).one()


clients = get_all_clients()

client = clients[0]
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
    _, user_column, _ = st.columns([1, 7, 1])
    user = get_user_data(client.UzytkownikId)
    with user_column:
        st.header("Client:")
        st.write("Surname:")
        st.write(f'{user.Nazwisko}')
        st.write("Name:")
        st.write(f'{user.Imie}')
        st.write("Date of birth:")
        st.write(f'{user.DataUr}')
        st.write("")

st.components.v1.html("""
    <script>
    const matches = parent.document.querySelectorAll("[data-testid='stVerticalBlock']");
    const match = matches[1];
    match.style.background = "#D6CCC2";
    match.style.textAlign = 'center';
    match.style.borderRadius = '10px';
    </script>
    """, height=0, width=0)

with col2:
    pass


