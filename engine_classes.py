from abc import ABC, abstractmethod
from connector import Connector
import requests
import os
import json


class Engine(ABC):
    @abstractmethod
    def get_request(self, keyword):
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
        отсутствует, то выводим то, что известно. Или выводим 0, если поле отсутствует"""
        if salary:
            if salary.get('to') and salary.get('from'):
                return {'from': salary['from'],
                        'to': salary['to']}
            elif salary.get('to') and not salary.get('from'):
                return {'from': 0, 'to': salary['to']}
            elif salary.get('from') and not salary.get('to'):
                return {'from': salary['from'], 'to': 0}
        else:
            return {'from': 0, 'to': 0}

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

        with open('hh_vacancy.json', 'w', encoding='utf-8') as file:
            json.dump(jobs, file, indent=2, ensure_ascii=False)


class SuperJob(Engine):
    @staticmethod
    def get_salary(salary):
        """Обрабатываем salary(зарплата): выводим 'от' и 'до', если оба поля присутствуют, если одно из полей
        отсутствует, то выволим то, что известно. Или выводим 0, если поле отсутствует"""
        if salary.get('payment_to') and salary.get('payment_from'):
            return {'from': salary['payment_from'],
                    'to': salary['payment_to']}
        elif salary.get('payment_to') and not salary.get('payment_from'):
            return {'from': 0, 'to': salary['payment_to']}
        elif salary.get('payment_from') and not salary.get('payment_to'):
            return {'from': salary['payment_from'], 'to': 0}
        return {'from': 0, 'to': 0}


    def get_request(self, keyword):
        jobs = []
        for i in range(5):
            api_key = os.getenv('superjob_key')
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers={'X-Api-App-Id': api_key},
                                    params={"keywords": keyword, "count": 100,
                                            "page": i})
            data = response.json()
            for i in data['objects']:
                jobs.append({
                    "name": i['profession'],
                    "company_name": i['firm_name'],
                    "url": i['link'],
                    "description": i['candidat'],
                    "salary": self.get_salary(i),
                })
        with open('sj_vacancy.json', 'w', encoding='utf-8') as file:
            json.dump(jobs, file, indent=2, ensure_ascii=False)
