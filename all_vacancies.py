import json

class All_vacancies:
    def vacancies_json(self):
        '''Создание общего файла с вакансиями'''
        file1 = json.loads(open('hh_vacancy.json', 'r', encoding='utf-8').read())
        file2 = json.loads(open('sj_vacancy.json', 'r', encoding='utf-8').read())

        file_all = file1 + file2

        with open('all_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(file_all, file, indent=2, ensure_ascii=False)