from PiktaDb import PiktaDb


p = PiktaDb(db_path="pikta_test.db")

# Метод, который создает базу данных, таблицы со связями и наполняет таблицы данными
# p.init_db(add_data=True)          # наполняет таблицы данными
p.init_db()             # не наполняет таблицы данными
