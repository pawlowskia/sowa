import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.create_database import Ksiazka, Autor, Autorstwo, Egzemplarz
from streamlit_modal import Modal

# Connect to the database
url = 'mysql+pymysql://root:password@localhost:13306/sowa'  # Update with your database connection details
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# Function to fetch all books from the database
def get_all_books():
    # return session.query(Ksiazka).all()
    # only return books that have at least one copy with status 'Dostepny'
    return session.query(Ksiazka).join(Egzemplarz).filter(Egzemplarz.Status == 'Dostepny').all()

# Fetch all books
books = get_all_books()
books_per_page = 10


def main():
    st.title("List of Books")

    page = st.session_state.page if 'page' in st.session_state else 0
    active_books = books[page * books_per_page:(page + 1) * books_per_page]

    for book in active_books:
        authors = session.query(Autor).join(Autorstwo).filter(Autorstwo.KsiazkaId == book.Id).all()
        authors_string = ''
        for author in authors:
            authors_string += author.Imie + ' ' + author.Nazwisko + ', '
        authors_string = authors_string[:-2]
        st.markdown(
            f"""
            <div style="background-color: #80A4ED; padding: 10px; border-radius: 10px;">
                <h3>{book.Tytul}</h3>
                <p><strong>ISBN:</strong> {book.ISBN}</p>
                <p><strong>Authors:</strong> {authors_string}</p>
                <p><strong>Publisher:</strong> {book.Wydawnictwo}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("")
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
