import unittest
from unittest.mock import patch, MagicMock
import login


class TestLoginFunction(unittest.TestCase):

    @patch("login.messagebox")
    @patch("login.store_main")
    @patch("login.storage_main")
    @patch("login.mydb.connect_db")
    def test_login_store_manager_success(self, mock_connect_db, mock_storage_main, mock_store_main, mock_messagebox):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("STORE MANAGER", "john123")
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        login.username_entry = MagicMock()
        login.password_entry = MagicMock()
        login.username_entry.get.return_value = "john123"
        login.password_entry.get.return_value = "secret"
        login.root = MagicMock()

        login.login()

        mock_store_main.assert_called_once_with("john123")
        mock_storage_main.assert_not_called()
        mock_messagebox.showerror.assert_not_called()

    @patch("login.messagebox")
    @patch("login.store_main")
    @patch("login.storage_main")
    @patch("login.mydb.connect_db")
    def test_login_storage_manager_success(self, mock_connect_db, mock_storage_main, mock_store_main, mock_messagebox):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("STORAGE MANAGER", "jane456")
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        login.username_entry = MagicMock()
        login.password_entry = MagicMock()
        login.username_entry.get.return_value = "jane456"
        login.password_entry.get.return_value = "pass456"
        login.root = MagicMock()

        login.login()

        mock_storage_main.assert_called_once_with("jane456")
        mock_store_main.assert_not_called()
        mock_messagebox.showerror.assert_not_called()

    @patch("login.messagebox")
    @patch("login.mydb.connect_db")
    def test_login_invalid_credentials(self, mock_connect_db, mock_messagebox):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn

        login.username_entry = MagicMock()
        login.password_entry = MagicMock()
        login.username_entry.get.return_value = "baduser"
        login.password_entry.get.return_value = "wrongpass"
        login.root = MagicMock()

        login.login()

        mock_messagebox.showerror.assert_called_with("Login Failed", "Invalid username or password")

    @patch("login.messagebox")
    @patch("login.mydb.connect_db", side_effect=Exception("Connection failed"))
    def test_login_db_exception(self, mock_connect_db, mock_messagebox):
        login.username_entry = MagicMock()
        login.password_entry = MagicMock()
        login.username_entry.get.return_value = "admin"
        login.password_entry.get.return_value = "adminpass"
        login.root = MagicMock()

        login.login()

        mock_messagebox.showerror.assert_called()
        args = mock_messagebox.showerror.call_args[0]
        self.assertIn("Database Error", args[0])
        self.assertIn("Connection failed", args[1])


if __name__ == '__main__':
    unittest.main()
