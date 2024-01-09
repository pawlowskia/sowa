from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from faker import Faker
import random

from create_database import Adres, Pracownik, Stanowisko, Uzytkownik, Klient, Autor, Zwrot, Ksiazka, Egzemplarz, \
    Wypozyczenie, MetodaPlatnosci, Platnosc, Autorstwo, ZwracanyEgzemplarz, ZamowionyEgzemplarz, PlatnoscKlient

Base = declarative_base()
fake = Faker()

engine = create_engine('mysql+pymysql://root:password@localhost:13306/sowa', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def generate_random_stanowisko():
    return {
        'Nazwa': fake.job()
    }


def generate_random_platnosc(g_metody_platnosci):
    return {
        'StatusPlatnosci': random.choice([True, False]),
        'MetodaPlatnosciId': random.choice(g_metody_platnosci).Id,
        'Kwota': fake.random_int(min=1, max=100)
    }


def generate_random_adres():
    return {
        'Ulica': fake.street_name(),
        'NrDomu': fake.building_number(),
        'NrMieszkania': fake.building_number(),
        'KodPocztowy': fake.zipcode(),
        'Miasto': fake.city(),
    }


def generate_random_uzytkownik(g_adresy):
    return {
        'Imie': fake.first_name(),
        'Nazwisko': fake.last_name(),
        'DataUr': fake.date_of_birth(),
        'Haslo': fake.password(),
        'AdresId': random.choice(g_adresy).Id,
        'Aktywny': random.choice([True, False]),
        'Pesel': fake.random_int(min=10000000000, max=99999999999),
        'Email': fake.email(),
    }


def generate_random_pracownik(g_stanowiska, g_uzytkownik):
    return {
        'DataZatr': fake.date_this_decade(),
        'StanowiskoId': random.choice(g_stanowiska).Id,
        'UzytkownikId': g_uzytkownik.Id
    }


def generate_random_platnosc_klient(g_klienci, g_platnosc):
    return {
        'KlientId': random.choice(g_klienci).Id,
        'PlatnoscId': g_platnosc.Id
    }


def generate_random_wypozyczenie(g_klienci, g_pracownicy):
    return {
        'DataUtworzenia': fake.date_this_year(),
        'DataZwrotu': fake.date_this_year(),
        'KlientId': random.choice(g_klienci).Id,
        'PracownikId': random.choice(g_pracownicy).Id
    }


def generate_random_zwrot(g_klienci, g_pracownicy):
    return {
        'DataUtworzenia': fake.date_this_year(),
        'DataZwrotu': fake.date_this_year(),
        'KlientId': random.choice(g_klienci).Id,
        'PracownikId': random.choice(g_pracownicy).Id
    }


def generate_random_autor():
    return {
        'Imie': fake.first_name(),
        'Nazwisko': fake.last_name()
    }


def generate_random_ksiazka():
    return {
        'Tytul': fake.sentence(),
        'ISBN': fake.isbn13(separator=''),
        'RokWydania': fake.random_int(min=1900, max=2023),
        'Wydawnictwo': fake.company()
    }


def generate_random_autorstwo(g_ksiazki, g_autorzy):
    return {
        'AutorId': random.choice(g_ksiazki).Id,
        'KsiazkaId': random.choice(g_autorzy).Id
    }


def generate_random_egzemplarz(g_ksiazki):
    return {
        'Status': random.choice(['Dostepny', 'Wypozyczony', 'Zarezerwowany']),
        'Stan': fake.random_int(min=1, max=5),
        'KsiazkaId': random.choice(g_ksiazki).Id
    }


def generate_random_zamowniony_egzemplarz(g_egzemplarze, g_wypozyczenia):
    return (
        random.choice(g_egzemplarze).Id,
        random.choice(g_wypozyczenia).Id
    )


def generate_random_zwracany_egzemplarz(g_egzemplarze, g_zwroty):
    return (
        random.choice(g_egzemplarze).Id,
        random.choice(g_zwroty).Id
    )


def generate_random_komentarz():
    return fake.text(max_nb_chars=200)


stanowiska = []
for _ in range(10):
    stanowiska.append(Stanowisko(**generate_random_stanowisko()))

session.add_all(stanowiska)

metody_platnosci = [MetodaPlatnosci(Metoda='gotówka'), MetodaPlatnosci(Metoda='karta'),
                    MetodaPlatnosci(Metoda='BLIK'), MetodaPlatnosci(Metoda='przelew')]
session.add_all(metody_platnosci)

adresy = []
for _ in range(5000):
    adresy.append(Adres(**generate_random_adres()))
session.add_all(adresy)
session.commit()

pracownicy = []
for _ in range(50):
    uzytkownik = Uzytkownik(**generate_random_uzytkownik(adresy))
    session.add(uzytkownik)
    session.commit()
    pracownicy.append(Pracownik(**generate_random_pracownik(stanowiska, uzytkownik)))
session.add_all(pracownicy)
session.commit()

klienci = []
for _ in range(2000):
    uzytkownik = Uzytkownik(**generate_random_uzytkownik(adresy))
    session.add(uzytkownik)
    session.commit()
    klienci.append(Klient(UzytkownikId=uzytkownik.Id))
session.add_all(klienci)
session.commit()

platnosci_klienci = []
for _ in range(100):
    platnosc = Platnosc(**generate_random_platnosc(metody_platnosci))
    session.add(platnosc)
    session.commit()
    platnosc_klient = PlatnoscKlient(**generate_random_platnosc_klient(klienci, platnosc))
    platnosci_klienci.append(platnosc_klient)
session.add_all(platnosci_klienci)
session.commit()

wypozyczenia = []
for _ in range(10000):
    wypozyczenia.append(Wypozyczenie(**generate_random_wypozyczenie(klienci, pracownicy)))
session.add_all(wypozyczenia)
session.commit()

zwroty = []
for _ in range(8000):
    zwroty.append(Zwrot(**generate_random_zwrot(klienci, pracownicy)))
session.add_all(zwroty)
session.commit()

autorzy = []
for _ in range(100):
    autorzy.append(Autor(**generate_random_autor()))
session.add_all(autorzy)
session.commit()

ksiazki = []
autorstwa = []
for _ in range(400):
    ksiazka = Ksiazka(**generate_random_ksiazka())
    session.add(ksiazka)
    ksiazki.append(ksiazka)
    session.commit()
    number_of_authors = random.choices([0, 1, 2, 3], [1, 15, 3, 1], k=1)[0]
    autorzy_ksiazki = random.sample(autorzy, k=number_of_authors)
    for i in range(0, number_of_authors):
        autorstwa.append(Autorstwo(AutorId=autorzy_ksiazki[i].Id, KsiazkaId=ksiazka.Id))
session.add_all(autorstwa)
session.commit()

egzemplarze = []
for _ in range(10000):
    egzemplarze.append(Egzemplarz(**generate_random_egzemplarz(ksiazki)))
session.add_all(egzemplarze)
session.commit()

zamowione_egzemplarze_set = set()
for _ in range(30000):
    zamowione_egzemplarze_set.add(generate_random_zamowniony_egzemplarz(egzemplarze, wypozyczenia))

zamowione_egzemplarze = []
for zamowiony_egzemplarz in zamowione_egzemplarze_set:
    zamowione_egzemplarze.append(
        ZamowionyEgzemplarz(EgzemplarzId=zamowiony_egzemplarz[0], WypozyczenieId=zamowiony_egzemplarz[1]))

session.add_all(zamowione_egzemplarze)

zwrocone_egzemplarze_set = set()
for _ in range(25000):
    zwrocone_egzemplarze_set.add(generate_random_zwracany_egzemplarz(egzemplarze, zwroty))

zwrocone_egzemplarze = []
for zwrocony_egzemplarz in zwrocone_egzemplarze_set:
    zwrocone_egzemplarze.append(ZwracanyEgzemplarz(ZwrotId=zwrocony_egzemplarz[1],
                                                   EgzemplarzId=zwrocony_egzemplarz[0],
                                                   Komentarz=generate_random_komentarz()))
session.add_all(zwrocone_egzemplarze)

session.commit()

session.close()
