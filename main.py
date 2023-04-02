import json
from engine_classes import SuperJob, HH
from vacancy import Vacancy
from all_vacancies import All_vacancies


if __name__ == '__main__':
    keyword = input('Введите ключевое слово для поиска вакансий: ')
    #Получаем 500 вакансий по ключевому слову с сайта HH.ru и сохраняем их в файл hh_vacancy.json
    hh = HH()
    hh_vacancies = hh.get_request(keyword)
    #Получаем 500 вакансий по ключевому слову с сайта SuperJob и сохраняем их в файл sj_vacancy.json
    sj = SuperJob()
    sj_vacancies = sj.get_request(keyword)

    data = All_vacancies()
    data.vacancies_json()

    print("По введеному ключевому слову собраны вакансии.\n"
          "Выберите номер для дальнейшего действия:\nНажмите 1, чтобы вывести количество вакансий, указанное пользователем\n"
          "Нажмите 2, чтобы вывести вакансии, в которых указана зарплата\n"
          "Нажмите 3, чтобы вывести вакансии с минимальной зарплатой равной или большей числу, указанному пользователем\n"
          "Нажмите 'stop', чтобы завершить программу")

    with open('all_vacancies.json', 'r', encoding='utf8') as file:
        vacancies_file = json.load(file)
        vacancies = []
        for item in vacancies_file:
            vacancy = Vacancy(item["name"], item["company_name"], item["url"], item["description"], item["salary"])
            vacancies.append(vacancy)

    user_input = input(f'Введите команду: ')

    while user_input != 'stop':
        if user_input == '1':
            number = int(input(f'Введите количество вакансий: '))
            for i in vacancies[:number]:
                print(i)
            user_input = input(f'Введите команду: ')

        if user_input == '2':
            jobs = []
            number = int(input(f'Введите количество вакансий: '))
            for i in vacancies:
                if i.salary['from'] and i.salary['to'] != 0:
                    jobs.append(i)
            for i in jobs[:number]:
                print(i)
            user_input = input(f'Введите команду: ')

        if user_input == '3':
            number = int(input(f'Введите минимальную зарплату: '))
            vac = int(input(f'Введите количество вакансий: '))
            job = []
            for i in vacancies:
                if i.salary['from'] >= number:
                    job.append(i)
            for i in job[:vac]:
                print(i)
            user_input = input(f'Введите команду: ')

    print('Работа окончена')