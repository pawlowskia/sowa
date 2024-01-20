import streamlit as st
from streamlit_option_menu import option_menu
from st_keyup import st_keyup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from streamlit_modal import Modal
from backend.database.create_database import Ksiazka, Autor, Autorstwo, Egzemplarz, Klient, Uzytkownik, PlatnoscKlient, \
    Platnosc

st.set_page_config(layout="wide")

url = 'mysql+pymysql://root:password@localhost:13306/sowa'
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'is_worker' not in st.session_state:
    st.session_state.is_worker = True


def get_all_copies(book_id):
    return session.query(Egzemplarz).join(Ksiazka).filter(Egzemplarz.KsiazkaId == book_id,
                                                          Egzemplarz.Status != "Niedostepny").all()


def delete_copy(copy_id):
    copy_to_delete = session.query(Egzemplarz).filter(Egzemplarz.Id == copy_id).first()
    copy_to_delete.Status = 'Niedostepny'
    session.commit()


def edit_book(book_id, title, authors, publisher, year):
    book_to_update = session.query(Ksiazka).filter(Ksiazka.Id == book_id).first()
    book_to_update.Tytul = title
    book_to_update.Wydawnictwo = publisher
    book_to_update.RokWydania = year
    book_authors = session.query(Autorstwo).filter(Autorstwo.KsiazkaId == book_id).all()
    for book_author in book_authors:
        session.delete(book_author)
    for author in authors:
        new_book_author = Autorstwo(AutorId=author.Id, KsiazkaId=book_id)
        session.add(new_book_author)
    session.commit()


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


def on_change(key):
    selection = st.session_state[key]
    # st.write(f"Selection changed to {selection}")
    if selection == "Notifications":
        modal = Modal(
            f"Notifications",
            key=f'modal-notif',
            padding=10,
            max_width=500
        )
        modal.open()

        if modal.is_open():
            with (modal.container()):
                notifications = session.query(Klient).join(PlatnoscKlient).join(Platnosc).filter(
                    Platnosc.StatusPlatnosci == False).all()
                for notification in notifications:
                    st.write(
                        f"Client {notification.Uzytkownik.Imie} {notification.Uzytkownik.Nazwisko} has to pay for the book {notification.Egzemplarz.Ksiazka.Tytul}")


navbar = None

if st.session_state.is_worker:
    navbar = option_menu(None, ["Home", "Account", "Search", "Reports", "Books", "Notifications"],
                         icons=['house', 'person-circle', "search", "file-earmark-bar-graph", "book", "bell"],
                         menu_icon="cast", default_index=0, orientation="horizontal", on_change=on_change, key='menu_5')
else:
    navbar = option_menu(None, ["Home", "Account", "Search", "Wallet", "Books", "Notifications"],
                         icons=['house', 'person-circle', "search", "wallet", "book", "bell"],
                         menu_icon="cast", default_index=0, orientation="horizontal", on_change=on_change, key='menu_5')

col1, col2 = st.columns([2, 5])
with col1:
    _, filter_column, _ = st.columns([1, 7, 1])
    with filter_column:
        st.header("Filter:")
        label_checkbox = st.write("Status")
        checkbox1 = st.checkbox("Available", value=True, disabled=False)
        checkbox2 = st.checkbox("Borrowed", value=False, disabled=False)
        checkbox3 = st.checkbox("Prepared", value=False, disabled=False)
        checkbox4 = st.checkbox("Unavailable", value=False, disabled=False)
        checkbox5 = st.checkbox("Reserved", value=False, disabled=False)
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
    col111, col222 = st.columns([8, 1])
    modal_add = Modal(
        "",
        key='modal_add',
        max_width=1000
    )
    with col111:
        st.title("List of Books")
    with col222:
        add_book_button = st.button("ADD BOOK")
        if add_book_button:
            modal_add.open()

    if modal_add.is_open():
        with modal_add.container():
            coli1, coli2, coli3 = st.columns([1, 8, 1])
            with coli2:
                title_preview = st.text_input("Title:")
                isbn_preview = st.text_input("ISBN:")
                author_preview = st.text_input("Author:")
                publisher_preview = st.text_input("Publisher:")
                year_preview = st.text_input("Year:")
                add_button = st.button("ADD")

    page = st.session_state.page if 'page' in st.session_state else 0
    active_books = st.session_state.books[page * books_per_page:(page + 1) * books_per_page]
    all_authors = session.query(Autor)

    for book in active_books:
        authors = session.query(Autor).join(Autorstwo).filter(Autorstwo.KsiazkaId == book.Id).all()
        authors_string = ''
        for author in authors:
            authors_string += author.Imie + ' ' + author.Nazwisko + ', '
        authors_string = authors_string[:-2]
        # Use Markdown to create a colored rectangle
        st.markdown(
            f"""
                    <div style="background-color: #E3D5CA; padding: 10px; border-radius: 10px;">
                            <h3>{book.Tytul}</h3>
                            <p><strong>ISBN:</strong> {book.ISBN}</p>
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
        col1, col2, col3 = st.columns([1, 1, 1])

        # Add row of buttons to the page
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            button_preview = st.button("PREVIEW", key=f'centered-{book.Id}')
        with col2:
            button_edit = st.button("EDIT", key=f'delete-{book.Id}')
        with col3:
            button_delete = st.button("DELETE", key=f'reserve-{book.Id}')
        modal_edit = Modal(
            "",
            key=f'{book.Id}-modal_edit',
            max_width=900
        )
        modal_preview = Modal(
            "",
            key=f'{book.Id}-modal_preview',
            max_width=900
        )
        if button_preview:
            modal_preview.open()
        if button_edit:
            modal_edit.open()

        confirm_delete_modal = Modal(
            "",
            key=f'{book.Id}-demo-confirm-delete-modal',

            # Optional
            padding=20,  # default value
            max_width=500  # default value
        )
        if button_delete:
            confirm_delete_modal.open()

        if confirm_delete_modal.is_open():
            with confirm_delete_modal.container():
                colum = st.columns([1, 8, 1])
                with colum[1]:
                    st.write(f"Choose copies of")
                    st.write(f'"{book.Tytul}" to delete')
                    copies = get_all_copies(book.Id)
                    copies_to_delete = st.multiselect("", options=copies)
                    confirm_delete_button = st.button("Confirm")
                if confirm_delete_button:
                    for copy in copies_to_delete:
                        delete_copy(copy.Id)
                    st.warning(f'{len(copies_to_delete)} copies status changed to inaccessible')

        if modal_preview.is_open():
            with modal_preview.container():
                col1, col2, col3 = st.columns([1, 8, 1])
                with col2:
                    title_preview = st.text_input("Title:", value=book.Tytul, disabled=True)
                    isbn_preview = st.text_input("ISBN:", value=book.ISBN, disabled=True)
                    author_preview = st.text_input("Author:", value=authors_string, disabled=True)
                    publisher_preview = st.text_input("Publisher:", value=book.Wydawnictwo, disabled=True)
                    year_preview = st.text_input("Year:", value=book.RokWydania, disabled=True)

        if modal_edit.is_open():
            with modal_edit.container():
                col1, col2, col3 = st.columns([1, 5, 1])

                with col2:
                    name_input = st.text_input("Title:", value=book.Tytul)
                    author_input = st.multiselect("Author:", options=all_authors, default=authors)
                    publisher_input = st.text_input("Publisher:", value=book.Wydawnictwo)
                    year_input = st.text_input("Year:", value=book.RokWydania)

                    confirm_edit_button = st.button("Save")

                    if confirm_edit_button:
                        edit_book(book.Id, name_input, author_input, publisher_input,
                                  year_input)
                        modal_edit.close()

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
    const match = matches[2];
    match.style.background = "#D6CCC2";
    match.style.textAlign = 'center';
    match.style.borderRadius = '10px';
    </script>
    """, height=0, width=0)

session.close()
