from dbmanager import DBManager


if __name__ == '__main__':
    db_init = DBManager()
    print(db_init.get_companies_and_vacancies_count())
    print(db_init.get_vacancies_with_keyword('Java Экология'))
    print(db_init.get_avg_salary())
    print(db_init.get_vacancies_with_higher_salary())
    print(db_init.get_all_vacancies())
