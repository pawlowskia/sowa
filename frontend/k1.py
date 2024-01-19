import streamlit as st
from datetime import datetime, timedelta

# Przykładowa lista dostępnych książek w systemie bibliotecznym
available_books = [
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "copies": 5},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "copies": 3},
    # Dodaj więcej książek według potrzeb
]

# Inicjalizacja danych użytkownika (tutaj można podać dane użytkownika po zalogowaniu)
user_id = 123
user_name = "John Doe"


# Funkcja do rezerwacji książki
def reserve_book(book):
    # Symulacja rezerwacji - tu można dodać logikę zapisującą dane rezerwacji do bazy danych
    st.success(f"Książka '{book['title']}' została pomyślnie zarezerwowana na twoje konto.")


# Funkcja do zwrotu książki
def return_book(book):
    # Symulacja zwrotu - tu można dodać logikę zapisującą datę zwrotu do bazy danych
    st.success(f"Książka '{book['title']}' została zwrócona.")


# Strona główna
def main():
    st.title("Wypożyczalnia Książek Online")

    # Logika wypożyczenia książki
    if st.button("Wypożycz Książkę"):
        # Krok 1: Wyświetlanie katalogu dostępnych książek
        st.header("Dostępne Książki")
        selected_book = st.selectbox("Wybierz książkę:", [book["title"] for book in available_books])

        # Krok 2-5: Filtry i rezerwacja książki
        if st.button("Zarezerwuj"):
            selected_book_data = next(book for book in available_books if book["title"] == selected_book)
            reserve_book(selected_book_data)

            # Krok 6: Rejestracja daty wypożyczenia i terminu zwrotu
            due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
            st.info(f"Książka musi być zwrócona do {due_date}.")

    # Logika scenariusza alternatywnego: Brak odbioru
    if st.button("Scenariusz Alternatywny: Brak Odbioru"):
        st.header("Scenariusz Alternatywny: Brak Odbioru")
        st.info("Sprawdzamy rezerwacje z przeszłości...")

        # Symulacja braku odbioru w przeciągu tygodnia
        overdue_book = available_books[0]
        overdue_date = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
        st.warning(f"Książka '{overdue_book['title']}' nie została odebrana do {overdue_date}. Automatyczny zwrot.")

        # Automatyczny zwrot książki
        return_book(overdue_book)

    # Logika anulowania wypożyczenia
    if st.button("Anuluj Wypożyczenie"):
        st.header("Anulowanie Wypożyczenia")

        # Symulacja wypożyczenia książki
        reserved_book = available_books[1]
        st.info(f"Masz zarezerwowaną książkę '{reserved_book['title']}'.")

        # Krok 7-8: Anulowanie wypożyczenia
        if st.button("Anuluj"):
            return_book(reserved_book)
            st.success("Wypożyczenie anulowane. Książka zwrócona.")


# Create two buttons
# button1 = st.button("Button 1")
# button2 = st.button("Button 2")

# Display buttons in a row
col1, col2, col3, col4, col5 = st.columns(5)  # Use st.columns for Streamlit version < 1.0

# Create a sidebar
with st.sidebar:
    st.markdown("### Button Box")

    # Place buttons inside the box
    button1 = st.button("aaa")
    if button1:
        st.write("Button 1 clicked!")

    button2 = st.button("bbb")
    if button2:
        st.write("Button 2 clicked!")

    button3 = st.button("ccc")
    if button3:
        st.write("Button 3 clicked!")

# Create a container
button_container = st.container()

# Place buttons inside the container
with button_container:
    st.markdown("### Button Box")

    button1 = st.button("Button a")
    if button1:
        st.write("Button 1 clicked!")

    button2 = st.button("Button b")
    if button2:
        st.write("Button 2 clicked!")

    button3 = st.button("Button c")
    if button3:
        st.write("Button 3 clicked!")

from typing import List

# def custom_button_box(title: str, buttons: List[str], background_color: str):
#     # Create a container with a specified background color
#     container_style = f"background-color: {background_color}; padding: 10px; border-radius: 5px;"
#     st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)
#
#     # Display title
#     st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
#
#     # Display buttons
#     for button_label in buttons:
#         if st.button(button_label):
#             st.write(f"{button_label} clicked!")
#
#     # Close the container
#     st.markdown("</div>", unsafe_allow_html=True)
#
# # Example usage
# custom_button_box("Button Box 1", ["Button 1", "Button 2", "Button 3"], "lightblue")
# custom_button_box("Button Box 2", ["Button A", "Button B", "Button C"], "lightcoral")


with col1:
    button1 = st.button("Button 1")
    if button1:
        st.write("Button 1 clicked!")

with col2:
    button2 = st.button("Button 2")
    if button2:
        st.write("Button 2 clicked!")
# make col4 red
# col4.markdown("<div style='float: left;'></div>", unsafe_allow_html=True)
with col4:
    button4 = st.button("Button 4")
    if button4:
        st.write("Button 4 clicked!")

with col5:
    button3 = st.button("Button 3")
    if button3:
        st.write("Button 3 clicked!")

st.markdown("# This is a Heading")

st.markdown("## This is a Subheading")

st.markdown("This is a paragraph with some **bold** and *italic* text.")

st.markdown("[Link to Streamlit](https://streamlit.io/)")

st.markdown("* Item 1\n* Item 2\n* Item 3")

if __name__ == "__main__":
    main()
