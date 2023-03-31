from abc import ABC, abstractmethod
from connector import Connector
import requests
from pprint import pprint


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = Connector(file_name)
        return connector


class HH(Engine):
    @staticmethod
    def get_salary(salary):
        """Обрабатываем salary(зарплата): выводим 'от' и 'до', если оба поля присутствуют, если одно из полей
        отсутствует, то выволим то, что известно. Или выводим 0, если поле отсутствует"""
        if salary:
            if salary.get('to') and salary.get('from'):
                return {'to': salary['to'],
                        'from': salary['from']}
            elif salary.get('to') and not salary.get('from'):
                return {'to': salary['to']}
            elif salary.get('from') and not salary.get('to'):
                return {'from': salary['from']}
        else:
            return 0


    def get_request(self, keyword):
        jobs = []
        for i in range(5):
            url = f"https://api.hh.ru/vacancies?text={keyword}"
            response = requests.get(url, params={'per_page': '100', 'page': i})
            data = response.json()
            for i in data['items']:
                jobs.append({
                    "name": i['name'],
                    "company_name": i['employer']['name'],
                    "url": i['alternate_url'],
                    "description": i['snippet']['requirement'],
                    "salary": self.get_salary(i.get('salary')),
                })

            return jobs
class SuperJob(Engine):
    def get_request(self):
        pass

hh = HH()
pprint(hh.get_request('python'))