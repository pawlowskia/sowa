from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

url = 'mysql+pymysql://root:password@localhost:13306/mysql'
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


Pracownik.stanowisko = relationship('Stanowisko', back_populates='pracownicy')
Pracownik.uzytkownik = relationship('Uzytkownik', back_populates='pracownicy')
Stanowisko.pracownicy = relationship('Pracownik', back_populates='stanowisko')
Uzytkownik.adres = relationship('Adres', back_populates='uzytkownicy')
Klient.uzytkownik = relationship('Uzytkownik', back_populates='klient')
Zwrot.klient = relationship('Klient', back_populates='zwroty')
Zwrot.pracownik = relationship('Pracownik', back_populates='zwroty')
Wypozyczenie.klient = relationship('Klient', back_populates='wypozyczenia')
Wypozyczenie.pracownik = relationship('Pracownik', back_populates='wypozyczenia')
Egzemplarz.ksiazka = relationship('Ksiazka', back_populates='egzemplarze')
ZamowionyEgzemplarz.egzemplarz = relationship('Egzemplarz', back_populates='zamowienia')
ZamowionyEgzemplarz.wypozyczenie = relationship('Wypozyczenie', back_populates='zamowienia')
Platnosc.metoda_platnosci = relationship('MetodaPlatnosci', back_populates='platnosci')
Platnosc.platnosc_klient = relationship('PlatnoscKlient', back_populates='platnosci')
Autor.autorstwa = relationship('Autorstwo', back_populates='autor')
Ksiazka.autorzy = relationship('Autorstwo', back_populates='ksiazka')
Zwrot.zwracane_egzemplarze = relationship('ZwracanyEgzemplarz', back_populates='zwrot')
Egzemplarz.zwracane_egzemplarze = relationship('ZwracanyEgzemplarz', back_populates='egzemplarz')
Egzemplarz.zamowienia = relationship('ZamowionyEgzemplarz', back_populates='egzemplarz')
Wypozyczenie.zamowienia = relationship('ZamowionyEgzemplarz', back_populates='wypozyczenie')

Base.metadata.create_all(engine)
