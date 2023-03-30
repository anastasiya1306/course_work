import json
import os


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, file):
        self.__data_file = file

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        # код для установки файла
        self.__data_file = value
        self.__connect()

    @staticmethod
    def is_file_exist(path):
        return os.path.isfile(path)

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        # проверка на наличие файла
        if not self.is_file_exist:
            raise FileNotFoundError('Файл не найден')
        try:
            with open(self.__data_file, 'r', encoding='utf-8') as file_path:
                data = json.load(file_path)
        except Exception:
            with open(self.data_file, 'w', encoding='utf-8') as file_path:
                json.dump([], file_path)



    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, 'r', encoding='utf8') as file:
            file_path = json.load(file)

        if isinstance(data, dict):
            file_path.append(data)
        elif isinstance(data, list):
            file_path.extend(data)

        with open(self.__data_file, 'w', encoding='utf8') as file:
            json.dump(file_path, file, ensure_ascii=False, indent=4)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        # считываем файл
        with open(self.__data_file, 'r', encoding='utf8') as file:
            file_path = json.load(file)
        data = []
        for i in file_path:
            for key, value in query.items():
                if i.get(key) == value:
                    data.append(i)
        return data

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not query:
            return

        with open(self.__data_file, 'r', encoding='utf8') as file:
            file_path = json.load(file)
        result = []
        for i in file_path:
            for key, value in query.items():
                if i.get(key) == value:
                    pass
                else:
                    result.append(i)

        with open(self.__data_file, 'w', encoding='utf8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == [data_for_file]

    df.delete({'id':1})
    data_from_file = df.select(dict())
    assert data_from_file == []