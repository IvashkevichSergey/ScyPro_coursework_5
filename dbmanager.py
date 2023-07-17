import psycopg2
from utils import DB_NAME, main
from config import config


class DBManager:
    """Класс для работы с базой данных по вакансиям"""
    def __init__(self):
        # Создаём нужную БД, получаем данные от api.hh.ru, заполняем БД данными по вакансиям
        main()
        # Список параметров для подключения к БД
        self.params = config()
        self.params.update({'dbname': DB_NAME})
        # Переменная для соединения с БД
        self.conn = None

    def get_companies_and_vacancies_count(self) -> list:
        """Метод получает список всех компаний и количество вакансий у каждой компании"""
        result = []
        try:
            self.conn = psycopg2.connect(**self.params)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                cur.execute("""
                            SELECT employers.employer_name, COUNT(*) as number_vacancies
                            FROM employers JOIN vacancies USING (employer_id)
                            GROUP BY employers.employer_name
                            """)
                result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return result

    def get_all_vacancies(self) -> list:
        """Метод получает список всех вакансий"""
        result = []
        try:
            self.conn = psycopg2.connect(**self.params)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                cur.execute("""
                            SELECT employers.employer_name, vacancies.vacancy_name, 
                                    vacancies.salary_from, vacancies.salary_to, vacancies.url
                            FROM employers JOIN vacancies USING (employer_id)
                            """)
                result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return result

    def get_avg_salary(self) -> list:
        """Метод получает среднюю зарплату по вакансиям"""
        result = []
        try:
            self.conn = psycopg2.connect(**self.params)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                cur.execute("""                            
                            SELECT ROUND(AVG((salary_from + salary_to)/2)) as average_salary
                            FROM vacancies
                            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                            """)
                result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return result

    def get_vacancies_with_higher_salary(self) -> list:
        """Метод получает список всех вакансий, у которых
        зарплата выше средней по всем вакансиям."""
        result = []
        try:
            self.conn = psycopg2.connect(**self.params)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                cur.execute("""                            
                            SELECT * FROM vacancies 
                            WHERE ((salary_from + salary_to)/2) > (
                                SELECT ROUND(AVG((salary_from + salary_to)/2)) as average_salary
                                FROM vacancies
                                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL)
                            """)
                result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return result

    def get_vacancies_with_keyword(self, keywords: str) -> list:
        """Метод получает список всех вакансий, в названии которых
        содержатся переданные в метод слова"""
        result = []
        try:
            self.conn = psycopg2.connect(**self.params)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                for word in keywords.split():
                    cur.execute(f"""                            
                                SELECT * FROM vacancies 
                                WHERE vacancy_name LIKE '%{word}%'
                                """)
                    result.extend(cur.fetchall())
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return result


if __name__ == '__main__':
    a = DBManager()
    print(a.get_companies_and_vacancies_count())
    print(a.get_vacancies_with_keyword('Java Экология'))
    print(a.get_avg_salary())
    print(a.get_vacancies_with_higher_salary())
    print(a.get_all_vacancies())
