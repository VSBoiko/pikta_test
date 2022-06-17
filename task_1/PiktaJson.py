import json


class PiktaJson:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def __get_json_data(self) -> dict:
        result = {}
        with open(self.json_file_path, "r", encoding="utf-8") as json_file:
            result = json.load(json_file)

        return result

    def get_table_from_json(self):
        json_data = self.__get_json_data()
        headers, values = json_data["headers"], json_data["values"]

        table = {}
        for header in headers:
            props = header["properties"] if "properties" in header else {}
            prop_x = int(props["X"]) if "X" in props else False
            prop_y = int(props["Y"]) if "Y" in props else False
            if prop_x and prop_y:
                table[(prop_x, prop_y)] = props["QuickInfo"]

        for value in values:
            props = value["properties"] if "properties" in value else {}
            prop_x = int(props["X"]) if "X" in props else False
            prop_y = int(props["Y"]) if "Y" in props else False
            if prop_x and prop_y:
                table[(prop_x, prop_y)] = props["Text"]

        table = dict(sorted(table.items(), key=lambda i: i[0]))

        return table
