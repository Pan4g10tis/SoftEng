import tkinter as tk
from PIL import Image, ImageTk
from classes import StoreManager,DataBase




def starter_page(frame, name, store):
   for widget in frame.winfo_children():
       widget.destroy()


   starter_text = f"""Welcome {name}!\nStore Info:\nAddress: {store.address}\nEmail: {store.email}\nPhone: {store.phone}"""
   starter_label = tk.Label(frame, text=starter_text, font=("Arial", 16), bg="white", justify="left")
   starter_label.pack(pady=10)




def store_main(username=""):
   mydb = DataBase("root", "root", "localhost", "indusstock")
   manager = StoreManager.create(mydb, username)
   store = manager.get_store(mydb)


   def show_content(action):
       if action == "Orders":
           get_orders(content_frame, store, mydb)
       if action == "Sales":
           get_sales(content_frame, store, mydb)
       if action == "Staff":
           get_workers(content_frame, store, mydb)
       if action == "Products":
           get_products(content_frame, store, mydb)
       if action == "Go Back":
           starter_page(content_frame, manager.name, store)


   window = tk.Tk()
   window.title("Store Manager Page")
   window.geometry("1500x1000")


   bg_image = Image.open("background.jpg")
   bg_image = bg_image.resize((1500, 1000), Image.LANCZOS)
   bg_photo = ImageTk.PhotoImage(bg_image)


   background_label = tk.Label(window, image=bg_photo)
   background_label.place(x=0, y=0, relwidth=1, relheight=1)


   content_frame = tk.Frame(window, bg="white", width=900, height=150)
   content_frame.place(x=300, y=20)


   sidebar = tk.Frame(window, bg="#f0f0f0", width=150)
   sidebar.pack(side="left", anchor="n", padx=10, pady=0)


   menu_label = tk.Label(sidebar, text="Menu", font=("Arial", 14, "bold"), bg="#ffffff")
   menu_label.pack(pady=(10, 20))


   button_texts = ["Orders", "Sales", "Staff", "Products", "Go Back"]
   for text in button_texts:
       btn = tk.Button(sidebar, text=text, width=15, pady=5, command=lambda t=text: show_content(t))
       btn.pack(pady=5)


   starter_page(content_frame, manager.name, store)


   window.mainloop()
