from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from classes import DataBase
from storemanager import store_main
from storagemanager import storage_main

# Globals for test mocking
root = None
username_entry = None
password_entry = None

mydb = DataBase("root", "root", "localhost", "indusstock")


def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        conn = mydb.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, username FROM manager WHERE manager.username = %s AND password = %s",
            (username, password),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            if root:
                root.destroy()
            if result[0] == "STORE MANAGER":
                store_main(result[1])
            elif result[0] == "STORAGE MANAGER":
                storage_main(result[1])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except Exception as err:
        messagebox.showerror("Database Error", str(err))


# GUI only runs when the script is executed directly
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Login")
    root.geometry("600x400")

    # Load background image
    try:
        from PIL import Image, ImageTk
        bg_image = Image.open("background.jpg")
        bg_image = bg_image.resize((600, 400), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        background_label = tk.Label(root, image=bg_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception:
        pass  # Skip background image if not found

    frame = tk.Frame(root, bg="white", bd=2)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(frame, text="Username:", bg="white").grid(row=0, column=0, pady=5, sticky='e')
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Password:", bg="white").grid(row=1, column=0, pady=5, sticky='e')
    password_entry = tk.Entry(frame, show='*')
    password_entry.grid(row=1, column=1, pady=5)

    login_button = tk.Button(frame, text="Login", command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()
