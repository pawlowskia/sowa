import streamlit as st
from streamlit_option_menu import option_menu
from st_keyup import st_keyup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from streamlit_modal import Modal
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

url = 'mysql+pymysql://root:password@localhost:13306/sowa'
engine = create_engine(url, echo=True)
connection = engine.connect()

Base = declarative_base()


class Adres(Base):
    __tablename__ = 'Adres'
    Id = Column(Integer, primary_key=True)
    Ulica = Column(String(100), nullable=False)
    NrDomu = Column(String(5), nullable=False)
    NrMieszkania = Column(String(5))
    KodPocztowy = Column(String(6), nullable=False)
    Miasto = Column(String(100), nullable=False)


class Pracownik(Base):
    __tablename__ = 'Pracownik'
    Id = Column(Integer, primary_key=True)
    DataZatr = Column(Date, nullable=False)
    StanowiskoId = Column(Integer, ForeignKey('Stanowisko.Id'), nullable=False)
    UzytkownikId = Column(Integer, ForeignKey('Uzytkownik.Id'), nullable=False)


class Stanowisko(Base):
    __tablename__ = 'Stanowisko'
    Id = Column(Integer, primary_key=True)
    Nazwa = Column(String(255), nullable=False)


class Uzytkownik(Base):
    __tablename__ = 'Uzytkownik'
    Id = Column(Integer, primary_key=True)
    Imie = Column(String(255), nullable=False)
    Nazwisko = Column(String(255), nullable=False)
    DataUr = Column(Date, nullable=False)
    Haslo = Column(String(255), nullable=False)
    AdresId = Column(Integer, ForeignKey('Adres.Id'))
    Aktywny = Column(Boolean)
    Pesel = Column(String(11))
    Email = Column(String(255))


class Klient(Base):
    __tablename__ = 'Klient'
    Id = Column(Integer, primary_key=True)
    UzytkownikId = Column(Integer, ForeignKey('Uzytkownik.Id'), nullable=False)


class Autor(Base):
    __tablename__ = 'Autor'
    Id = Column(Integer, primary_key=True)
    Imie = Column(String(255), nullable=False)
    Nazwisko = Column(String(255), nullable=False)

    def __str__(self):
        return f"{self.Imie} {self.Nazwisko}"


class Zwrot(Base):
    __tablename__ = 'Zwrot'
    Id = Column(Integer, primary_key=True)
    DataUtworzenia = Column(Date, nullable=False)
    DataZwrotu = Column(Date)
    KlientId = Column(Integer, ForeignKey('Klient.Id'), nullable=False)
    PracownikId = Column(Integer, ForeignKey('Pracownik.Id'))


class Ksiazka(Base):
    __tablename__ = 'Ksiazka'
    Id = Column(Integer, primary_key=True)
    Tytul = Column(String(255), nullable=False)
    ISBN = Column(String(13), nullable=False)
    RokWydania = Column(Integer)
    Wydawnictwo = Column(String(255))


class Egzemplarz(Base):
    __tablename__ = 'Egzemplarz'
    Id = Column(Integer, primary_key=True)
    KsiazkaId = Column(Integer, ForeignKey('Ksiazka.Id'))
    Status = Column(Enum('Dostepny', 'Wypozyczony', 'Zarezerwowany'))
    Stan = Column(Integer)


class Wypozyczenie(Base):
    __tablename__ = 'Wypozyczenie'
    Id = Column(Integer, primary_key=True)
    DataUtworzenia = Column(Date, nullable=False)
    DataZwrotu = Column(Date)
    KlientId = Column(Integer, ForeignKey('Klient.Id'), nullable=False)
    PracownikId = Column(Integer, ForeignKey('Pracownik.Id'))


class MetodaPlatnosci(Base):
    __tablename__ = 'MetodaPlatnosci'
    Id = Column(Integer, primary_key=True)
    Metoda = Column(String(255), nullable=False)


class Platnosc(Base):
    __tablename__ = 'Platnosc'
    Id = Column(Integer, primary_key=True)
    StatusPlatnosci = Column(Boolean, nullable=False, default=False)
    MetodaPlatnosciId = Column(Integer, ForeignKey('MetodaPlatnosci.Id'))
    Kwota = Column(Integer, nullable=False)


class Autorstwo(Base):
    __tablename__ = 'Autorstwo'
    AutorId = Column(Integer, ForeignKey('Autor.Id'), primary_key=True)
    KsiazkaId = Column(Integer, ForeignKey('Ksiazka.Id'), primary_key=True)


class ZwracanyEgzemplarz(Base):
    __tablename__ = 'ZwracanyEgzemplarz'
    ZwrotId = Column(Integer, ForeignKey('Zwrot.Id'), primary_key=True)
    EgzemplarzId = Column(Integer, ForeignKey('Egzemplarz.Id'), primary_key=True)
    Komentarz = Column(String(255))


class ZamowionyEgzemplarz(Base):
    __tablename__ = 'ZamowionyEgzemplarz'
    EgzemplarzId = Column(Integer, ForeignKey('Egzemplarz.Id'), primary_key=True)
    WypozyczenieId = Column(Integer, ForeignKey('Wypozyczenie.Id'), primary_key=True)


class PlatnoscKlient(Base):
    __tablename__ = 'PlatnoscKlient'
    KlientId = Column(Integer, ForeignKey('Klient.Id'), primary_key=True)
    PlatnoscId = Column(Integer, ForeignKey('Platnosc.Id'), primary_key=True)


Ksiazka.autorzy = relationship('Autorstwo', back_populates='ksiazka')
Autor.ksiazki = relationship('Autorstwo', back_populates='autor')
Autorstwo.ksiazka = relationship('Ksiazka', back_populates='autorzy')
Autorstwo.autor = relationship('Autor', back_populates='ksiazki')
Ksiazka.egzemplarze = relationship('Egzemplarz', back_populates='ksiazka')
Egzemplarz.ksiazka = relationship('Ksiazka', back_populates='egzemplarze')
Egzemplarz.zwroty = relationship('ZwracanyEgzemplarz', back_populates='egzemplarz')
ZwracanyEgzemplarz.egzemplarz = relationship('Egzemplarz', back_populates='zwroty')
ZwracanyEgzemplarz.zwrot = relationship('Zwrot', back_populates='egzemplarze')
Zwrot.egzemplarze = relationship('ZwracanyEgzemplarz', back_populates='zwrot')
Egzemplarz.zamowienia = relationship('ZamowionyEgzemplarz', back_populates='egzemplarz')
ZamowionyEgzemplarz.egzemplarz = relationship('Egzemplarz', back_populates='zamowienia')
ZamowionyEgzemplarz.wypozyczenie = relationship('Wypozyczenie', back_populates='egzemplarze')
Wypozyczenie.egzemplarze = relationship('ZamowionyEgzemplarz', back_populates='wypozyczenie')
Stanowisko.pracownicy = relationship('Pracownik', back_populates='stanowisko')
Pracownik.stanowisko = relationship('Stanowisko', back_populates='pracownicy')
Pracownik.zwroty = relationship('Zwrot', back_populates='pracownik')
Zwrot.pracownik = relationship('Pracownik', back_populates='zwroty')
Pracownik.wypozyczenia = relationship('Wypozyczenie', back_populates='pracownik')
Wypozyczenie.pracownik = relationship('Pracownik', back_populates='wypozyczenia')
Klient.zwroty = relationship('Zwrot', back_populates='klient')
Zwrot.klient = relationship('Klient', back_populates='zwroty')
Klient.wypozyczenia = relationship('Wypozyczenie', back_populates='klient')
Wypozyczenie.klient = relationship('Klient', back_populates='wypozyczenia')
Klient.platnosci = relationship('PlatnoscKlient', back_populates='klient')
PlatnoscKlient.klient = relationship('Klient', back_populates='platnosci')
PlatnoscKlient.platnosc = relationship('Platnosc', back_populates='klienci')
Platnosc.klienci = relationship('PlatnoscKlient', back_populates='platnosc')
Platnosc.metodaPlatnosci = relationship('MetodaPlatnosci', back_populates='platnosci')
MetodaPlatnosci.platnosci = relationship('Platnosc', back_populates='metodaPlatnosci')
Adres.uzytkownicy = relationship('Uzytkownik', back_populates='adres')
Uzytkownik.adres = relationship('Adres', back_populates='uzytkownicy')

Base.metadata.create_all(engine)


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
                notifications = session.query(Klient).join(PlatnoscKlient).join(Platnosc).filter(Platnosc.StatusPlatnosci == False).all()
                for notification in notifications:
                    st.write(f"Client {notification.Uzytkownik.Imie} {notification.Uzytkownik.Nazwisko} has to pay for the book {notification.Egzemplarz.Ksiazka.Tytul}")


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
    const match = matches[2];
    match.style.background = "#D6CCC2";
    match.style.textAlign = 'center';
    match.style.borderRadius = '10px';
    </script>
    """, height=0, width=0)

session.close()
