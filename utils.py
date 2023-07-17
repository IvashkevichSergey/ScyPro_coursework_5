import requests
import psycopg2
from config import config

# Название для новой БД
DB_NAME = 'hh_vacancies'


def main():
    # Получаем список параметров для подключения к БД
    params = config()
    # Создаём переменную для соединения с БД
    conn = None

    create_database(params, DB_NAME)
    print(f"БД {DB_NAME} успешно создана")
    # Обновляем имя БД в словаре с конфигурационными параметрами
    params.update({'dbname': DB_NAME})

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_employers_table(cur)
                print("Таблица employers успешно создана")
                create_vacancies_table(cur)
                print("Таблица vacancies успешно создана")

                vacancies = get_vacancies()
                fill_employers_table(cur, vacancies)
                print("Данные в employers успешно добавлены")

                fill_vacancies_table(cur, vacancies)
                print("Данные в vacancies успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params: dict, db_name: str) -> None:
    """Функция для создания базы данных для хранения вакансий"""
    # Создаём соединение с существующей БД postgres
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True

    # Создаём новую БД
    with conn.cursor() as cur:
        cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
        cur.execute(f'CREATE DATABASE {db_name}')
    conn.close()


def create_employers_table(cur) -> None:
    """Функция создаёт в БД таблицу employers"""
    cur.execute("""
            CREATE TABLE employers(
                employer_id integer PRIMARY KEY,
                employer_name varchar(100),
                url varchar(100)         
            )
        """)


def create_vacancies_table(cur) -> None:
    """Функция создаёт в БД таблицу vacancies"""
    cur.execute("""
            CREATE TABLE vacancies(
                vacancy_id serial PRIMARY KEY,
                vacancy_name varchar(100),
                url varchar(100),
                salary_from integer,
                salary_to integer,          
                employer_id integer REFERENCES employers
            )
        """)


def get_vacancies() -> list:
    """Функция получает список вакансий от работодателей"""
    list_with_vacancies = []
    employers_ids = [1304253, 4372397, 8155, 3884354, 1868342, 14809, 1479818, 581293, 1947, 2516882, 2393]

    print('Идёт сбор вакансий на сайте HeadHunter.ru...', end='')

    # Собираем вакансии у каждого из работодателей из списка employers_ids
    for employer in employers_ids:
        # Словарь с параметрами для поискового запроса
        search_params = {'employer_id': employer,
                         'per_page': 100,
                         'page': 0}

        response = requests.get('https://api.hh.ru/vacancies', params=search_params).json()

        # Проходим по всем страницам с искомым запросом и сохраняем все вакансии в список
        while search_params['page'] < 10 and response['items']:
            for vacancy in response['items']:

                # Отсекаем вакансии, в которых ЗП указана не в рублях
                if vacancy.get('salary'):
                    if vacancy.get('salary').get('currency') != 'RUR':
                        continue

                list_with_vacancies.append(vacancy)
            search_params['page'] += 1
            response = requests.get('https://api.hh.ru/vacancies', params=search_params).json()
        print('.', end='')
    print()
    return list_with_vacancies


def fill_employers_table(cur, vacancies: list) -> None:
    """Функция заполняет данными таблицу employers"""
    employers = []
    for vacancy in vacancies:
        employer_id = vacancy['employer']['id']
        employer_name = vacancy['employer']['name']
        employer_url = vacancy['employer']['alternate_url']
        if (employer_id, employer_name, employer_url) not in employers:
            employers.append((employer_id, employer_name, employer_url))
            cur.execute("""INSERT INTO employers VALUES (%s, %s, %s)""",
                        (employer_id, employer_name, employer_url))


def fill_vacancies_table(cur, vacancies: list) -> None:
    """Функция заполняет данными таблицу vacancies"""
    for vacancy in vacancies:
        vacancy_name = vacancy['name']
        vacancy_url = vacancy['alternate_url']
        # Делаем доп. проверку для ЗП, т.к. она не всегда указана
        if vacancy.get('salary'):
            salary_from = vacancy['salary'].get('from')
            salary_to = vacancy['salary'].get('to')
        else:
            salary_from = salary_to = None
        employer_id = vacancy['employer']['id']
        cur.execute("""
                    INSERT INTO vacancies (vacancy_name, url, salary_from, salary_to, employer_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (vacancy_name, vacancy_url, salary_from, salary_to, employer_id))
