import unittest
from unittest.mock import MagicMock, patch
from datetime import date

from classes import Store, Product, StoreOrder, StoreSale, Worker, DataBase

class TestStoreMethods(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=DataBase)
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.db.connect_db.return_value = self.connection
        self.connection.cursor.return_value = self.cursor

    def test_show_orders(self):
        store = Store(1, "123 Street", "email@test.com", "12345678")

        # Set up mock data
        self.cursor.fetchall.side_effect = [
            [(1, 'HIGH', 'PENDING', date.today(), None)],
            [(101, 5)]
        ]

        orders = store.show_orders(self.db)

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].products[0], 101)
        self.assertEqual(orders[0].amounts[0], 5)

    def test_show_stats(self):
        store = Store(1, "123 Street", "email@test.com", "12345678")

        self.cursor.fetchone.return_value = [10]
        count = store.show_stats(self.db, "2023-01-01", "2023-12-31")
        self.assertEqual(count, 10)

class TestProductMethods(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=DataBase)
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.db.connect_db.return_value = self.connection
        self.connection.cursor.return_value = self.cursor

    def test_insert_product(self):
        product = Product(None, "Product A", "Brand X", "Type Y", 100.0, 0)

        self.cursor.fetchone.return_value = [123]

        product.insert_product(self.db)

        self.assertEqual(product.id, 123)
        self.assertTrue(self.cursor.execute.called)
        self.assertTrue(self.connection.commit.called)

    def test_delete_product(self):
        product = Product(5, "Product B", "Brand Y", "Type Z", 99.99, 20)
        product.delete_product(self.db)

        self.assertTrue(self.connection.commit.called)
        self.assertEqual(self.cursor.execute.call_count, 3)

class TestStoreOrder(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=DataBase)
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.db.connect_db.return_value = self.connection
        self.connection.cursor.return_value = self.cursor

    def test_insert_order(self):
        order = StoreOrder(None, 1, "HIGH", "PENDING", None, None, [10], [2])
        self.cursor.fetchone.return_value = [77]

        order.insert_order(self.db)

        self.assertEqual(order.id, 77)
        self.assertTrue(self.connection.commit.called)

class TestStoreSale(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=DataBase)
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.db.connect_db.return_value = self.connection
        self.connection.cursor.return_value = self.cursor

    def test_insert_sale(self):
        sale = StoreSale(None, 1, date.today(), [10], [3])
        self.cursor.fetchone.return_value = [15]

        sale.insert_sale(self.db)

        self.assertEqual(self.cursor.execute.call_count, 5)
        self.assertTrue(self.connection.commit.called)


if __name__ == '__main__':
    unittest.main()
