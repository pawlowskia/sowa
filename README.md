# Biblioteka SOWA
Projekt PO

Pobierz docker, potem (Windows - GIT Bash; MacOS/Linux - domyślna konsola):
```
$ docker pull mysql:latest
```
Obraz dockerowy bazy danych tworzymy za pomocą komendy:
```
$ docker run -p 13306:3306 --name sowa -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE_NAME=sowa -d mysql:latest
```
Następnie przy uruchomieniu skryptu mogą wystąpić różnorakie błędy, np. 
```
RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods
```
Należy wtedy doinstalować odpowiednie pakiety, np. tu `cryptography`
