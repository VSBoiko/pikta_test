import os.path
import json


class PiktaJson:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def get_format_table(self) -> list:
        """
        Получить данные таблицы списком строк

        :return: списком строк таблицы
        [
            [
                'Сумма во ВВ',
                'Внутренняя валюта',
                'Код налога',
                'Счет Главной книги'
            ],
            [
                ' 3 500,00',
                'RUB',
                'CH',
                '32-020010'
            ]
        ]
        """

        table = self.__get_table_from_json()
        format_table = []
        prev_x = False
        i = -1
        for key, value in table.items():
            x = key[0]
            if prev_x != x:
                format_table.append([])
                prev_x = x
                i += 1
            format_table[i].append(value)

        return format_table

    def __get_json_data(self) -> dict:
        result = {}
        if os.path.isfile(self.json_file_path):
            with open(self.json_file_path, "r", encoding="utf-8") as json_file:
                result = json.load(json_file)

        return result

    def __get_table_from_json(self) -> dict:
        json_data = self.__get_json_data()
        headers = json_data["headers"] if "headers" in json_data else {}

        table = {}
        for header in headers:
            props = header["properties"] if "properties" in header else {}
            prop_x = int(props["X"]) if "X" in props else False
            prop_y = int(props["Y"]) if "Y" in props else False
            if prop_x and prop_y:
                table[(prop_y, prop_x)] = props["QuickInfo"]

        values = json_data["values"] if "values" in json_data else {}
        for value in values:
            props = value["properties"] if "properties" in value else {}
            prop_x = int(props["X"]) if "X" in props else False
            prop_y = int(props["Y"]) if "Y" in props else False
            if prop_x and prop_y:
                table[(prop_y, prop_x)] = props["Text"]

        if table != {}:
            result = dict(sorted(table.items(), key=lambda i: i[0]))
        else:
            result = {}

        return result
