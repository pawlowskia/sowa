import time

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.create_database import Ksiazka, Autor, Autorstwo, Base, Egzemplarz
from streamlit_modal import Modal

# Connect to the database
url = 'mysql+pymysql://root:password@localhost:13306/sowa'  # Update with your database connection details
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def get_all_books():
    return session.query(Ksiazka).all()


def get_all_copies(book_id):
    # return session.query(Ksiazka).all()
    # only return books that have at least one copy with status 'Dostepny'
    return session.query(Egzemplarz).join(Ksiazka).filter(Egzemplarz.KsiazkaId == book_id,
                                                          Egzemplarz.Status != "Niedostepny").all()


def delete_copy(copy_id):
    copy_to_delete = session.query(Egzemplarz).filter(Egzemplarz.Id == copy_id).first()
    copy_to_delete.Status = 'Niedostepny'
    session.commit()


def edit_book(book_id, title, isbn, authors, publisher, year):
    book_to_update = session.query(Ksiazka).filter(Ksiazka.Id == book_id).first()
    book_to_update.Tytul = title
    if len(isbn) < 14:
        book_to_update.ISBN = isbn
    book_to_update.Wydawnictwo = publisher
    book_to_update.RokWydania = year
    book_authors = session.query(Autorstwo).filter(Autorstwo.KsiazkaId == book_id).all()
    for book_author in book_authors:
        session.delete(book_author)
    for author in authors:
        new_book_author = Autorstwo(AutorId=author.Id, KsiazkaId=book_id)
        session.add(new_book_author)
    session.commit()


# Fetch all books
books = get_all_books()
books_per_page = 10


def main():
    st.title("List of Books")

    # Get the page from session state
    page = st.session_state.page if 'page' in st.session_state else 0
    active_books = books[page * books_per_page:(page + 1) * books_per_page]
    all_authors = session.query(Autor)
    # Display books in a scrollable list
    for book in active_books:
        authors = session.query(Autor).join(Autorstwo).filter(Autorstwo.KsiazkaId == book.Id).all()
        authors_string = ''
        for author in authors:
            authors_string += author.Imie + ' ' + author.Nazwisko + ', '
        authors_string = authors_string[:-2]
        # Use Markdown to create a colored rectangle
        st.markdown(
            f"""
                    <div style="background-color: #D5BDAF; padding: 10px; border-radius: 10px;">
                        <table>
                            <tr>
                                <td>
                                    <h3>{book.Tytul}</h3>
                                    <p><strong>ISBN:</strong> {book.ISBN}</p>
                                    <p><strong>Authors:</strong> {authors_string}</p>
                                </td>   
                            </tr>
                        </table>
                    </div>
                    """,
            unsafe_allow_html=True
        )
        st.markdown("")
        # Add row of buttons to the page
        # st.button("Reserve", key=f'reserve-{book.Id}')
        col1, col2, col3 = st.columns([1, 1, 1])
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
        # Add row of buttons to the page
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            button_preview = st.button("Preview", key=f'centered-{book.Id}')
        with col2:
            button_edit = st.button("Edit", key=f'delete-{book.Id}')
        with col3:
            button_delete = st.button("Delete Copies", key=f'reserve-{book.Id}')
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
        confirm_edit_modal = Modal(
            "",
            key=f'{book.Id}-confirm-edit-modal',

            # Optional
            padding=20,  # default value
            max_width=300  # default value
        )
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

                    return_button = st.button("Back")

                    if return_button:
                        modal_preview.close()

        if modal_edit.is_open():
            with modal_edit.container():
                col1, col2, col3 = st.columns([1, 8, 1])
                with col2:
                    name_input = st.text_input("Title:", value=book.Tytul)
                    isbn_input = st.text_input("ISBN:", value=book.ISBN)
                    author_input = st.multiselect("Author:", options=all_authors, default=authors)
                    publisher_input = st.text_input("Publisher:", value=book.Wydawnictwo)
                    year_input = st.text_input("Year:", value=book.RokWydania)

                    col4, col5, col6 = st.columns([1, 7, 1])
                    with col4:
                        return_button = st.button("Back")

                    if return_button:
                        modal_edit.close()

                    with col6:
                        confirm_edit_button = st.button("Save")

                    if confirm_edit_button:
                        confirm_edit_modal.open()

                    if confirm_edit_modal.is_open():
                        with confirm_edit_modal.container():
                            st.write("Are you sure?")
                            col111, col112 = st.columns([1, 4])
                            with col111:
                                yes = st.button("Yes")
                                if yes:
                                    edit_book(book.Id, name_input, isbn_input, author_input, publisher_input,
                                              year_input)
                                    confirm_edit_modal.close()

    st.write("---")  # Separator between books

    prev_page_col, separator, next_page_col = st.columns([1, 4, 1])

    if page > 0:
        with prev_page_col:
            if st.button(f"Previous Page ({max(page - 1, 0)})"):
                st.session_state.page = max(0, page - 1)
                st.rerun()
    with next_page_col:
        if st.button(f"Next Page ({page + 1})"):
            st.session_state.page += 1
            st.rerun()


# Close the database session
session.close()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 0

if __name__ == "__main__":
    main()
