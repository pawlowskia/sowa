import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.create_database import Klient, Uzytkownik, Autorstwo, Egzemplarz, Autor,\
    Ksiazka, ZamowionyEgzemplarz, Wypozyczenie
from st_keyup import st_keyup
from streamlit_option_menu import option_menu
from streamlit_modal import Modal

st.set_page_config(layout="wide")

url = 'mysql+pymysql://root:password@localhost:13306/sowa'
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def get_all_clients():
    return session.query(Klient).all()


def get_user_data(user_id):
    return session.query(Uzytkownik).where(Uzytkownik.Id == user_id).one()


clients = get_all_clients()

client = clients[0]


def get_books(g_client):
    return (session.query(Egzemplarz).join(ZamowionyEgzemplarz).join(Wypozyczenie).join(Klient).join(Ksiazka)
            .where(Klient.Id == g_client.Id)
            .where(Ksiazka.Id == Egzemplarz.KsiazkaId)
            .all())


def get_wypozyczenie(egzemplarz_id):
    return session.query(ZamowionyEgzemplarz).join(Egzemplarz).where(egzemplarz_id == ZamowionyEgzemplarz.EgzemplarzId).all()


if 'page_b3' not in st.session_state:
    st.session_state.page_b3 = 0
if 'is_worker' not in st.session_state:
    st.session_state.is_worker = True
if 'books_b3' not in st.session_state:
    st.session_state.books_b3 = get_books(client)


navbar = option_menu(None, ["Home", "Account", "Search", "Reports", "Books", "Notifications"],
                     icons=['house', 'person-circle', "search", "file-earmark-bar-graph", "book", "bell"],
                     menu_icon="cast", default_index=0, orientation="horizontal", key='menu_5')


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
        for _ in range(20):
            st.write("")

st.components.v1.html("""
    <script>
    const matches = parent.document.querySelectorAll("[data-testid='stVerticalBlock']");
    const match = matches[2];
    match.style.background = "#D6CCC2";
    match.style.textAlign = 'center';
    match.style.borderRadius = '10px';
    </script>
    """, height=0, width=0)

with col2:
    st.title("List of Books")
    books_per_page = 3

    page_b3 = st.session_state.page_b3 if 'page_b3' in st.session_state else 0
    active_books = st.session_state.books_b3[page_b3 * books_per_page:(page_b3 + 1) * books_per_page]

    for book in active_books:
        authors = session.query(Autor).join(Autorstwo).filter(Autorstwo.KsiazkaId == book.KsiazkaId).all()
        ksiazka = session.query(Ksiazka).join(Egzemplarz).filter(Ksiazka.Id == book.KsiazkaId).all()[0]
        authors_string = ''
        for author in authors:
            authors_string += author.Imie + ' ' + author.Nazwisko + ', '
        authors_string = authors_string[:-2]
        st.markdown(
            f"""
                    <div style="background-color: #E3D5CA; padding: 10px; border-radius: 10px;">
                        <h3>{ksiazka.Tytul}</h3>
                        <p><strong>Authors:</strong> {authors_string}</p>
                    </div>
                    """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <style>
                div.stButton {
                    text-align: center;
                }
            </style>
            """
            , unsafe_allow_html=True
        )
        modal = Modal(
            f"Chosen book:<br/> {ksiazka.Tytul}",
            key=f'modal-{book.Id}',
            padding=10,
            max_width=500
        )
        modal2 = Modal(
            f"Chosen book:<br/> {ksiazka.Tytul}",
            key=f'modal2-{book.Id}',
            padding=10,
            max_width=500
        )
        colReturn, _, colPenalty = st.columns([1, 3.5, 1])
        with colReturn:
            open_modal = st.button("RETURN", key=f'return-{book.Id}')
            if open_modal:
                modal.open()
        with colPenalty:
            open_penalty_modal = st.button("ADD PENALTY", key=f'penalty-{book.Id}')
            if open_penalty_modal:
                modal2.open()

        if modal.is_open():
            with modal.container():
                col11, col12, col13 = st.columns([1, 1.5, 1])
                with col11:
                    for _ in range(10):
                        st.write("")
                    if st.button("Return"):
                        modal.close()

                with col12:
                    percentage = st_keyup("Type percentage of damage:", key="1")

                with col13:
                    for _ in range(10):
                        st.write("")
                    if st.button("Approve"):
                        print('wfgfa')
                        for a in get_wypozyczenie(book.Id):
                            print('wfgfa')
                            print(a)
                            session.delete(a)
                        st.session_state.books_b3 = get_books(client)
                        modal.close()

        if modal2.is_open():
            with modal2.container():
                col11, col12, col13 = st.columns([1, 1.5, 1])
                with col11:
                    for _ in range(10):
                        st.write("")
                    if st.button("Return"):
                        modal2.close()

                with col12:
                    percentage = st_keyup("Type penalty amount:", key="2")

                with col13:
                    for _ in range(10):
                        st.write("")
                    if st.button("Approve"):
                        modal2.close()

    prev_page_col, separator, next_page_col = st.columns([1, 4, 1])

    if page_b3 > 0:
        with prev_page_col:
            if st.button(f"Previous Page ({max(page_b3 - 1, 0)})"):
                st.session_state.page_b3 = max(0, page_b3 - 1)
                st.rerun()
    if page_b3 < len(st.session_state.books_b3) // books_per_page - 1:
        with next_page_col:
            if st.button(f"Next Page ({page_b3 + 1})"):
                st.session_state.page_b3 += 1
                st.rerun()

session.close()
