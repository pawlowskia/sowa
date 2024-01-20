import time

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.create_database import Ksiazka, Autor, Autorstwo, Base

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
        button_click = st.button("Centered Button", key=f'centered-{book.Id}')
    with col2:
        st.button("Delete", key=f'delete-{book.Id}')
    with col3:
        st.button("Reserve", key=f'reserve-{book.Id}')

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
