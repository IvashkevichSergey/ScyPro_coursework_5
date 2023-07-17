-- Запрос на список всех компаний и количество вакансий у каждой компании
SELECT employers.employer_name, COUNT(*)
FROM employers JOIN vacancies USING (employer_id)
GROUP BY employers.employer_name

-- Запрос на список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT employers.employer_name, vacancies.vacancy_name,
vacancies.salary_from, vacancies.salary_to, vacancies.url
FROM employers JOIN vacancies USING (employer_id)

-- Запрос на среднюю зарплату по вакансиям
SELECT ROUND(AVG((salary_from + salary_to)/2)) as average_salary
FROM vacancies
WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL

-- Запрос на список всех вакансий, у которых зарплата выше средней по всем вакансиям
 SELECT * FROM vacancies
 WHERE ((salary_from + salary_to)/2) > (
     SELECT ROUND(AVG((salary_from + salary_to)/2)) as average_salary
     FROM vacancies
     WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
     )

-- Запрос на список всех вакансий, в названии которых содержатся переданные в метод слова
for word in keywords.split():
    cur.execute(f"""SELECT * FROM vacancies WHERE vacancy_name LIKE '%{word}%'""")