import time

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.create_database import Ksiazka, Autor, Autorstwo, Base
from streamlit_modal import Modal

# Connect to the database
url = 'mysql+pymysql://root:password@localhost:13306/sowa'  # Update with your database connection details
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Function to fetch all books from the database
def get_all_books():
    return session.query(Ksiazka).all()


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
                    <div style="background-color: #80A4ED; padding: 10px; border-radius: 10px;">
                        <table>
                            <tr>
                                <td>
                                    <h3>{book.Tytul}</h3>
                                    <p><strong>ISBN:</strong> {book.ISBN}</p>
                                    <p><strong>Authors:</strong> {authors_string}</p>
                                    <p><strong>Publisher:</strong> {book.Wydawnictwo}</p>
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
        # Add row of buttons to the page
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            button_preview = st.button("Preview", key=f'centered-{book.Id}')
        with col2:
            button_edit =  st.button("Edit", key=f'delete-{book.Id}')
        with col3:
            button_delete = st.button("Delete", key=f'reserve-{book.Id}')
        modal_edit = Modal(
            f'{book.Tytul}',
            key=f'{book.Id}-modal_edit',
            max_width=900
        )
        modal_preview = Modal(
            f'{book.Tytul}',
            key=f'{book.Id}-modal_preview',
            max_width=900
        )
        if button_preview:
            modal_preview.open()
        if button_edit:
            modal_edit.open()
        confirm_edit_modal = Modal(
            "",
            key=f'{book.Id}-demo-modal',

            # Optional
            padding=20,  # default value
            max_width=300  # default value
        )
        confirm_delete_modal = Modal(
            "",
            key=f'{book.Id}-demo-modal',

            # Optional
            padding=20,  # default value
            max_width=500  # default value
        )
        if button_delete:
            confirm_delete_modal.open()

        if confirm_delete_modal.is_open():
            with confirm_delete_modal.container():
                st.write(f'Are you sure you want delete "{book.Tytul}"')
                col11,col12,col13 = st.columns([1,2,2])
                with col11:
                    no = st.button("Cancel")
                with col13:
                    yes = st.button("Confirm")
                if no:
                    confirm_delete_modal.close()


        if modal_preview.is_open():
            with modal_preview.container():
                col1, col2, col3 = st.columns([1, 8, 1])
                with col2:
                    isbn_preview = st.text_input("ISBN:", value=book.ISBN, disabled=True)
                    author_preview = st.text_input("Author:",value=authors_string, disabled=True)
                    publisher_preview = st.text_input("Publisher:", value=book.Wydawnictwo, disabled=True)
                    year_preview = st.text_input("Year:", value= book.RokWydania, disabled=True)

                    return_button = st.button("Back")

                    if return_button:
                        modal_preview.close()

        if modal_edit.is_open():
            with modal_edit.container():
                col1, col2, col3 = st.columns([1, 8, 1])
                with col2:
                    isbn_input = st.text_input("ISBN:", value=book.ISBN)
                    name_input = st.text_input("Title:", value=book.Tytul)
                    author_input = st.multiselect("Author:",options=all_authors)
                    publisher_input = st.text_input("Publisher:", value=book.Wydawnictwo)
                    year_input = st.text_input("Year:", value= book.RokWydania)

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
                            yes = st.button("Yes")

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
