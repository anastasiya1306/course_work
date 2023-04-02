class Vacancy:
    __slots__ = ('name', 'company_name', 'url', 'description', 'salary')

    def __init__(self, name, company_name, url, description, salary):
        self.name = name
        self.company_name = company_name
        self.url = url
        self.description = description
        self.salary = salary


    def __str__(self):
       return f'Название вакансии: {self.name}\nОрганизация: {self.company_name}\n'\
              f'Ссылка на вакансию:{self.url}\n'\
              f'Описание вакансии: {self.description}\n'\
              f'Зарплата:{self.salary["from"]} - {self.salary["to"]}\n'