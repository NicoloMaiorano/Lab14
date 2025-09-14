from database.DB_connect import DBConnect
from model.ordine import Order
from model.store import Store


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        lista = []

        query = """SELECT * FROM stores"""

        cursor.execute(query)

        for c in cursor:
            x = Store(**c)
            lista.append(x)

        conn.close()
        cursor.close()
        return lista

    @staticmethod
    def getOrdiniStore(store_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        lista = []

        query = """SELECT * FROM orders
                    WHERE store_id = %s"""

        cursor.execute(query, (store_id, ))

        for c in cursor:
            x = Order(**c)
            lista.append(x)

        conn.close()
        cursor.close()
        return lista

    @staticmethod
    def getOggettiOrdine(order_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """ SELECT SUM(quantity) as somma FROM order_items
                    WHERE order_id = %s"""
        cursor.execute(query, (order_id, ))

        for c in cursor:
            somma = c["somma"]

        print(f"somma: {somma}")

        conn.close()
        cursor.close()
        return somma
