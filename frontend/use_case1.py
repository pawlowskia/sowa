import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from sowa.database.create_database import Zwrot, Klient, Egzemplarz, ZwracanyEgzemplarz

# Tworzenie sesji
engine = create_engine('mysql+pymysql://root:password@localhost:13306/sowa')
Session = sessionmaker(bind=engine)
session = Session()

# Strona główna
st.title("Zwrot Książki")

# Formularz dla użytkownika
klient_id = st.number_input("Podaj ID Klienta:", min_value=1)
egzemplarz_id = st.number_input("Podaj ID Egzemplarza:", min_value=1)

if st.button("Zwróć Książkę"):
    # Sprawdzenie czy egzemplarz jest aktualnie wypożyczony
    egzemplarz = session.query(Egzemplarz).filter_by(Id=egzemplarz_id, Status='Wypozyczony').first()

    if egzemplarz:
        # Ustawienie daty zwrotu na aktualną datę
        data_zwrotu = datetime.now()

        # Tworzenie nowego zwrotu
        nowy_zwrot = Zwrot(
            DataUtworzenia=datetime.now(),
            DataZwrotu=data_zwrotu,
            KlientId=klient_id,
            PracownikId=None  # Możesz uzupełnić, jeśli zwrot jest dokonywany przez pracownika
        )

        # Dodanie zwrotu do bazy danych
        session.add(nowy_zwrot)

        # Dodanie powiązania zwrotu z egzemplarzem
        zwracany_egzemplarz = ZwracanyEgzemplarz(ZwrotId=nowy_zwrot.Id, EgzemplarzId=egzemplarz_id, Komentarz="Brak uwag")
        session.add(zwracany_egzemplarz)

        # Zaktualizowanie statusu egzemplarza na dostępny
        egzemplarz.Status = 'Dostepny'

        # Zatwierdzenie transakcji
        session.commit()

        st.success("Książka została pomyślnie zwrócona.")
    else:
        st.error("Egzemplarz nie jest obecnie wypożyczony.")
