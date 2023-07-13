import requests, json


class HeadHunterAPI:
    """Класс для работы с API сайта hh.ru"""

    def __init__(self):
        self.list_with_vacancies = []

    def get_vacancies(self):
        """
        Метод для формирования файла со списком вакансий по ключевому слову
        """
        # Словарь с параметрами для поискового запроса
        search_params = {'employer_id': 1479818,
                         'per_page': 100,
                         'page': 0}

        list_companies_ids = [1304253, 4372397, 8155, 3884354, 1868342, 14809, 1479818, 581293, 1947, 2516882, 2393]


        response = requests.get('https://api.hh.ru/vacancies', params=search_params).json()

        # Создаём переменную для хранения вакансий - объектов класса Vacancy
        self.list_with_vacancies = []
        # Проходим по всем страницам с искомым запросом и сохраняем все вакансии в список
        print('Идёт поиск на сайте HeadHunter.ru...', end='')
        while search_params['page'] < 5 and response['items']:
            for vacancy in response['items']:
                self.list_with_vacancies.append(vacancy)

        #         if vacancy.get('salary'):
        #             if vacancy.get('salary').get('currency') != 'RUR':
        #                 continue
        #         self.list_with_vacancies.append(
        #             Vacancy(vacancy_name=vacancy['name'],
        #                     vacancy_url=vacancy['alternate_url'],
        #                     salary_from=None if not vacancy.get('salary') else vacancy.get(
        #                         'salary').get(
        #                         'from'),
        #                     salary_to=None if not vacancy.get('salary') else vacancy.get(
        #                         'salary').get('to'),
        #                     job_description=vacancy['snippet']['responsibility'])
        #         )
            search_params['page'] += 1
            response = requests.get('https://api.hh.ru/vacancies', params=search_params).json()
            print('.', end='')
        # print(f'\nНа сайте HeadHunter.ru по Вашему запросу найдено {len(self.list_with_vacancies)} вакансий')
        return self.list_with_vacancies

a = HeadHunterAPI()
b = a.get_vacancies()
with open('abc.json', 'w', encoding='utf-8') as f:
    json.dump(b, f, ensure_ascii=False, indent=2)
