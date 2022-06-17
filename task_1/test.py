from PiktaJson import PiktaJson
from PiktaExcel import PiktaExcel


json1 = PiktaJson("test1.json")
json1_table = json1.get_format_table()

json2 = PiktaJson("test2.json")
json2_table = json2.get_format_table()

json3 = PiktaJson("test3.json")
json3_table = json3.get_format_table()

excel_path = "test1.xlsx"
ex = PiktaExcel(excel_path)
ex.create_excel()
ex.add_worksheet("1", json1_table)
ex.add_worksheet("2", json2_table)
ex.add_worksheet("3", json3_table)
