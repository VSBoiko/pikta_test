from PiktaDb import PiktaDb


p = PiktaDb(db_path="pikta_test.db")


# Метод, который создает базу данных, таблицы со связями и наполняет таблицы данными
# p.init_db(add_data=True)          # наполняет таблицы данными
p.init_db()             # не наполняет таблицы данными


# Метод, который возвращает результаты запроса: список клиентов с общей суммой их покупки
print("\tCписок клиентов с общей суммой их покупки:")
clients_amount = p.get_clients_amount()
for amount in clients_amount:
    print(f"{amount['client_name']} - {amount['amount']}")


# Метод, который возвращает результаты запроса: список клиентов, которые купили телефон
print("\n\tCписок клиентов, которые купили телефон:")
who_bought_phone = p.get_who_bought_phone()
for client in who_bought_phone:
    print(f"{client['client_name']}")
