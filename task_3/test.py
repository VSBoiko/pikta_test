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


# Метод, который возвращает результаты запроса: список товаров с количеством их заказа
print("\n\tCписок товаров с количеством их заказа:")
products = p.get_products_order_quantity()
for product in products:
    print(f"{product['product_name']} - {product['orders_count']}")


# console:
# 	Cписок клиентов с общей суммой их покупки:
# Александр - 9999.9
# Дмитрий - 318.87
# Иван - 10636.76
# Константин - 10317.89
#
# 	Cписок клиентов, которые купили телефон:
# Константин
# Александр
# Иван
#
# 	Cписок товаров с количеством их заказа:
# Кофе - 2
# Кружка - 2
# Мяч - 2
# Ручка - 2
# Телефон - 3
