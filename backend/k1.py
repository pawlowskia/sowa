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

books = books[:10]  # Limit to first 10 books

def main():
    st.title("List of Books")

    # Display books in a scrollable list
    for book in books:
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
                        <td>
                            <p><strong>Year:</strong> {book.RokWydania}</p>
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
                    color: #80A4ED
                    
                }
            </style>
            """
            , unsafe_allow_html=True
        )
        with col1:
            # Use CSS style to center the button horizontall

            # Add the centered button
            button_click = st.button("Centered Button", key=f'centered-{book.Id}')
        with col2:
            st.button("Delete", key=f'delete-{book.Id}')
        with col3:
            st.button("Reserve", key=f'reserve-{book.Id}')

        st.write("---")  # Separator between books

# Close the database session
session.close()

if __name__ == "__main__":
    main()
