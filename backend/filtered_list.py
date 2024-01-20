import streamlit as st
from streamlit_option_menu import option_menu
from st_keyup import st_keyup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from database.create_database import Ksiazka, Autor, Autorstwo, Egzemplarz, Klient, Uzytkownik, PlatnoscKlient, Platnosc
from streamlit_modal import Modal

st.set_page_config(layout="wide")

url = 'mysql+pymysql://root:password@localhost:13306/sowa'  # Update with your database connection details
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'is_worker' not in st.session_state:
    st.session_state.is_worker = True


def get_books(statuses, author, title, year, publisher):
    print(statuses, author, title, year, publisher)

    return (session.query(Ksiazka).join(Egzemplarz).join(Autorstwo).join(Autor)
            .filter(Autor.Imie.like(f'%{author}%'))
            .filter(Egzemplarz.Status.in_(statuses))
            .filter(Ksiazka.Tytul.like(f'%{title}%'))
            .filter(Ksiazka.RokWydania.like(f'%{year}%'))
            .filter(Ksiazka.Wydawnictwo.like(f'%{publisher}%'))
            .all())

books_per_page = 3

if 'books' not in st.session_state:
    st.session_state.books = get_books(["Dostepny"], '', '', '', '')

navbar = None


if st.session_state.is_worker:
    navbar = option_menu(None, ["Home", "Account", "Search", "Reports", "Books", "Notifications"],
                                icons=['house', 'person-circle', "search", "file-earmark-bar-graph", "book", "bell"],
                                menu_icon="cast", default_index=0, orientation="horizontal", key='menu_5')
else:
    navbar = option_menu(None, ["Home", "Account", "Search", "Wallet", "Books", "Notifications"],
                              icons=['house', 'person-circle', "search", "wallet", "book", "bell"],
                              menu_icon="cast", default_index=0, orientation="horizontal", key='menu_5')

col1, col2 = st.columns([2, 5])
with col1:
    _, filter_column, _ = st.columns([1, 7, 1])
    with filter_column:
        st.header("Filter:")
        label_checkbox = st.write("Status")
        checkbox1 = st.checkbox("Available", value=True, disabled=True)
        checkbox2 = st.checkbox("Borrowed", value=False, disabled=True)
        checkbox3 = st.checkbox("Prepared", value=False, disabled=True)
        checkbox4 = st.checkbox("Unavailable", value=False, disabled=True)
        checkbox5 = st.checkbox("Reserved", value=False, disabled=True)
        with_debounce = st_keyup("Author", debounce=500, key="1")
        with_debounce2 = st_keyup("Title", debounce=500, key="2")
        with_debounce3 = st_keyup("Publication Year", debounce=500, key="3")
        with_debounce4 = st_keyup("Publisher", debounce=500, key="4")
        button_apply = st.button("Apply", key="apply-filter")
        st.write("")

        statuses = []
        if checkbox1:
            statuses.append('Dostepny')
        if checkbox2:
            statuses.append('Wypozyczony')
        if checkbox3:
            statuses.append('Przygotowany')
        if checkbox4:
            statuses.append('Niedostepny')
        if checkbox5:
            statuses.append('Zarezerwowany')

        if button_apply:
            st.session_state.books = get_books(statuses, with_debounce, with_debounce2, with_debounce3, with_debounce4)
            st.session_state.page = 0
            st.rerun()


with col2:
    st.title("List of Books")

    page = st.session_state.page if 'page' in st.session_state else 0
    active_books = st.session_state.books[page * books_per_page:(page + 1) * books_per_page]

    for book in active_books:
        authors = session.query(Autor).join(Autorstwo).filter(Autorstwo.KsiazkaId == book.Id).all()
        authors_string = ''
        for author in authors:
            authors_string += author.Imie + ' ' + author.Nazwisko + ', '
        authors_string = authors_string[:-2]
        st.markdown(
            f"""
                <div style="background-color: #E3D5CA; padding: 10px; border-radius: 10px;">
                    <h3>{book.Tytul}</h3>
                    <p><strong>Authors:</strong> {authors_string}</p>
                </div>
                """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <style>
                .st-emotion-cache-es6upy {
                    background-color: #80A4BB

                }

                div.stButton {
                    text-align: center;
                }
            </style>
            """
            , unsafe_allow_html=True
        )

        modal = Modal(
            f"Chosen book:<br/> {book.Tytul}",
            key=f'modal-{book.Id}',
            padding=10,
            max_width=500
        )
        open_modal = st.button("RESERVE", key=f'open-{book.Id}')
        if open_modal:
            modal.open()

        if modal.is_open():
            with modal.container():
                copies = session.query(Egzemplarz).filter_by(KsiazkaId=book.Id, Status='Dostepny').all()
                st.write(f"Copies available for reservation: {len(copies)}")
                if st.button("Reserve"):
                    # reserve the first copy
                    copy = copies[0]
                    copy.Status = 'Zarezerwowany'
                    session.commit()
                    st.success("Book reserved")


    prev_page_col, separator, next_page_col = st.columns([1, 4, 1])

    if page > 0:
        with prev_page_col:
            if st.button(f"Previous Page ({max(page - 1, 0)})"):
                st.session_state.page = max(0, page - 1)
                st.rerun()
    if page < len(st.session_state.books) // books_per_page - 1:
        with next_page_col:
            if st.button(f"Next Page ({page + 1})"):
                st.session_state.page += 1
                st.rerun()

st.components.v1.html("""
    <script>
    const matches = parent.document.querySelectorAll("[data-testid='stVerticalBlock']");
    const match = matches[1];
    match.style.background = "#D6CCC2";
    match.style.textAlign = 'center';
    match.style.borderRadius = '10px';
    </script>
    """, height=0, width=0)

session.close()
