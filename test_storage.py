import unittest
from unittest.mock import MagicMock, patch
from datetime import date
import tkinter as tk

from storagemanager import (
    get_store_orders, get_storage_orders, get_workers, get_products, get_stores, starter_page
)

class MockOrder:
    def __init__(self, id, store, status, priority, start_date, end_date):
        self.id = id
        self.store = store
        self.status = status
        self.priority = priority
        self.start_date = start_date
        self.end_date = end_date
        self.products = ["Prod A"]
        self.amounts = [10]

    def cancel_order(self, db):
        self.status = "CANCELED"

    def confirm_order(self, db):
        self.status = "CONFIRMED"

    def send_order(self, db):
        self.status = "SENT"

    def complete_order(self, db):
        self.status = "COMPLETED"

    def insert_order(self, db):
        pass

class MockProduct:
    def __init__(self, id, name, manufacturer, prod_type, price, stock):
        self.id = id
        self.name = name
        self.manufacturer = manufacturer
        self.type = prod_type
        self.price = price
        self.stock = stock

    def insert_product(self, db):
        pass

    def delete_product(self, db):
        pass

    def storage_sent_stats(self, db, sid, start, end):
        return 5

    def storage_order_stats(self, db, sid, start, end):
        return 7

class MockWorker:
    def __init__(self, id, name, surname, email, phone):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone

    def show_store_shift(self, db, date_str):
        return [(self.surname, "09:00", "17:00")]

class MockStore:
    def __init__(self, id, address, email, phone):
        self.id = id
        self.address = address
        self.email = email
        self.phone = phone

    def show_stats(self, db, start_date, end_date):
        return 10

class TestStorageManagerUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create hidden Tkinter root window for variable creation
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_starter_page(self):
        frame = MagicMock()
        storage = MagicMock(address="123 St", email="email@test.com", phone="12345")
        starter_page(frame, "Alice", storage)
        frame.winfo_children.assert_called()

    @patch("storagemanager.tk.StringVar")
    def test_get_store_orders(self, mock_stringvar):
        mock_stringvar.return_value = MagicMock()
        frame = MagicMock()
        storage = MagicMock()
        mydb = MagicMock()
        storage.show_store_orders.return_value = [MockOrder(1, 1, "PENDING", "HIGH", date.today(), None)]

        get_store_orders(frame, storage, mydb)
        storage.show_store_orders.assert_called()

    @patch("storagemanager.tk.StringVar")
    def test_get_storage_orders(self, mock_stringvar):
        mock_stringvar.return_value = MagicMock()
        frame = MagicMock()
        storage = MagicMock()
        mydb = MagicMock()
        storage.show_storage_orders.return_value = [MockOrder(2, 1, "PENDING", "NORMAL", date.today(), None)]

        get_storage_orders(frame, storage, mydb)
        storage.show_storage_orders.assert_called()

    @patch("storagemanager.tk.StringVar")
    def test_get_workers(self, mock_stringvar):
        mock_stringvar.return_value = MagicMock()
        frame = MagicMock()
        storage = MagicMock()
        mydb = MagicMock()
        storage.show_workers.return_value = [MockWorker(1, "Bob", "Smith", "bob@test.com", "123")]

        get_workers(frame, storage, mydb)
        storage.show_workers.assert_called()

    @patch("storagemanager.tk.StringVar")
    def test_get_products(self, mock_stringvar):
        mock_stringvar.return_value = MagicMock()
        frame = MagicMock()
        storage = MagicMock()
        mydb = MagicMock()
        storage.show_products.return_value = [MockProduct(1, "Widget", "Co", "TOOLS", 10.0, 50)]

        get_products(frame, storage, mydb)
        storage.show_products.assert_called()

    def test_get_stores(self):
        frame = MagicMock()
        mydb = MagicMock()
        conn = MagicMock()
        cursor = MagicMock()
        cursor.fetchall.return_value = [(1, "Addr", "email@test.com", "123")]
        conn.cursor.return_value = cursor
        mydb.connect_db.return_value = conn

        get_stores(frame, mydb)
        mydb.connect_db.assert_called()
        cursor.execute.assert_called()

if __name__ == '__main__':
    unittest.main()
