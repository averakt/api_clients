# API сервис для добавления/получения/обновления/удаления клиентов на Python3.8 and FastAPI

## Как запустить

Run

````
$ docker-compose --compatibility up --scale users=1 -d --build
````

Использование `--compatibility` чтобы имя приложения docker имело имя с подчеркиваниями.

Документация по работе с API http://127.0.0.1:8001/users/docs или http://127.0.0.1:8001/users/redoc 

## Как запустить тесты

````
$ python -m pytest app/tests
````
или

````
$ docker-compose exec app python -m pytest app/tests
````
