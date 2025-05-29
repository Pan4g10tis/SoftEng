import unittest
from unittest.mock import MagicMock, patch
from datetime import date
import tkinter as tk

from storemanager import (
    get_orders, get_sales, get_workers, get_products, starter_page
)

class MockProduct:
    def __init__(self, id, name, manufacturer, prod_type, price, stock):
        self.id = id
        self.name = name
        self.manufacturer = manufacturer
        self.type = prod_type
        self.price = price
        self.stock = stock

    def store_sale_stats(self, db, store_id, start_date, end_date):
        return 10

    def store_order_stats(self, db, store_id, start_date, end_date):
        return 5

    def insert_notes(self, db, store_id, note):
        pass

    def show_notes(self, db, store_id):
        return ["Note 1", "Note 2"]

class MockWorker:
    def __init__(self, id, name, surname, email, phone):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone

    def show_store_shift(self, db, date_str):
        return [(self.surname, "09:00", "17:00")]

class MockSale:
    def __init__(self, id, date):
        self.id = id
        self.date = date
        self.products = ["Product A"]
        self.amounts = [5]

    def insert_sale(self, db):
        pass

class MockOrder:
    def __init__(self, id, status, priority, start_date, end_date):
        self.id = id
        self.status = status
        self.priority = priority
        self.start_date = start_date
        self.end_date = end_date
        self.products = ["Product A"]
        self.amounts = [1]

    def cancel_order(self, db):
        self.status = "CANCELED"

    def complete_order(self, db):
        self.status = "COMPLETED"

    def insert_order(self, db):
        pass

class TestStoreManagerUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create hidden root window for tkinter variables to work
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    @patch("storemanager.tk.Entry")
    @patch("storemanager.ttk.Combobox")
    def test_get_orders(self, mock_combobox, mock_entry):
        frame = MagicMock()
        store = MagicMock()
        store.show_orders.return_value = [MockOrder(1, "PENDING", "HIGH", date.today(), date.today())]
        store.show_products.return_value = [MockProduct(1, "Prod A", "Manu", "TOOLS", 10.0, 100)]

        get_orders(frame, store, MagicMock())
        store.show_orders.assert_called()

    @patch("storemanager.tk.Entry")
    def test_get_sales(self, mock_entry):
        frame = MagicMock()
        store = MagicMock()
        store.show_sales.return_value = [MockSale(1, date.today())]

        get_sales(frame, store, MagicMock())
        store.show_sales.assert_called()

    def test_get_workers(self):
        frame = MagicMock()
        store = MagicMock()
        store.show_workers.return_value = [MockWorker(1, "John", "Doe", "john@example.com", "123")]

        get_workers(frame, store, MagicMock())
        store.show_workers.assert_called()

    @patch("storemanager.tk.Entry")
    @patch("storemanager.ttk.Combobox")
    def test_get_products(self, mock_combobox, mock_entry):
        frame = MagicMock()
        store = MagicMock()
        store.show_products.return_value = [MockProduct(1, "Prod A", "Manu", "TOOLS", 10.0, 100)]

        get_products(frame, store, MagicMock())
        store.show_products.assert_called()

    def test_starter_page(self):
        frame = MagicMock()
        starter_page(frame, "John", MagicMock(address="Addr", email="mail@test.com", phone="999"))
        frame.winfo_children.assert_called()

if __name__ == '__main__':
    unittest.main()
