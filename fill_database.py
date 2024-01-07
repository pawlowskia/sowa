from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from faker import Faker
import random

from sowa.create_database import Adres, Pracownik, Stanowisko, Uzytkownik, Klient, Autor, Zwrot, Ksiazka, Egzemplarz, \
    Wypozyczenie, MetodaPlatnosci, Platnosc, Autorstwo, ZwracanyEgzemplarz, ZamowionyEgzemplarz, PlatnoscKlient

Base = declarative_base()
fake = Faker()

engine = create_engine('mysql+pymysql://root:password@localhost:13306/mysql', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def generate_random_data():
    return {
        'Ulica': fake.street_name(),
        'NrDomu': fake.building_number(),
        'NrMieszkania': fake.building_number(),
        'KodPocztowy': fake.zipcode(),
        'Miasto': fake.city(),

        'DataZatr': fake.date_this_decade(),

        'Nazwa': fake.job(),

        'Imie': fake.first_name(),
        'Nazwisko': fake.last_name(),
        'DataUr': fake.date_of_birth(),
        'Haslo': fake.password(),
        'Aktywny': random.choice([True, False]),
        'Pesel': fake.random_int(min=10000000000, max=99999999999),
        'Email': fake.email(),

        'Tytul': fake.sentence(),
        'ISBN': fake.isbn13(),
        'RokWydania': fake.random_int(min=1900, max=2023),
        'Wydawnictwo': fake.company(),

        'Status': random.choice(['Dostepny', 'Wypozyczony', 'Zarezerwowany']),
        'Stan': fake.random_int(min=1, max=5),

        'DataUtworzenia': fake.date_this_year(),
        'DataZwrotu': fake.date_this_year(),

        'Metoda': fake.word(),

        'Kwota': fake.random_int(min=1, max=100),

        'StatusPlatnosci': random.choice([True, False])
    }

stanowiska = []
for _ in range(10):
    stanowiska.append(Stanowisko(**generate_random_data()))

print(stanowiska)

# for _ in range(100):
#     adres = Adres(**generate_random_data())
#     pracownik = Pracownik(**generate_random_data())
#     stanowisko = Stanowisko(**generate_random_data())
#     uzytkownik = Uzytkownik(**generate_random_data())
#     klient = Klient(**generate_random_data())
#     autor = Autor(**generate_random_data())
#     zwrot = Zwrot(**generate_random_data())
#     ksiazka = Ksiazka(**generate_random_data())
#     egzemplarz = Egzemplarz(**generate_random_data())
#     wypozyczenie = Wypozyczenie(**generate_random_data())
#     metoda_platnosci = MetodaPlatnosci(**generate_random_data())
#     platnosc = Platnosc(**generate_random_data())
#     autorstwo = Autorstwo(**generate_random_data())
#     zwracany_egzemplarz = ZwracanyEgzemplarz(**generate_random_data())
#     zamowiony_egzemplarz = ZamowionyEgzemplarz(**generate_random_data())
#     platnosc_klient = PlatnoscKlient(**generate_random_data())
#
#     session.add_all([adres, pracownik, stanowisko, uzytkownik, klient, autor, zwrot, ksiazka,
#                     egzemplarz, wypozyczenie, metoda_platnosci, platnosc, autorstwo, zwracany_egzemplarz,
#                     zamowiony_egzemplarz, platnosc_klient])

# Commit the changes to the database
session.commit()

# Close the session
session.close()
