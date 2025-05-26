import tkinter as tk
from PIL import Image, ImageTk
from classes import StorageManager,DataBase




def starter_page(frame, name, storage):
   for widget in frame.winfo_children():
       widget.destroy()


   starter_text = (f"Welcome {name}!\nStorage Info:\nAddress: {storage.address}\nEmail: {storage.email}\n"
                   f"Phone: {storage.phone}")
   starter_label = tk.Label(frame, text=starter_text, font=("Arial", 16), bg="white", justify="left")
   starter_label.pack(pady=10)




def storage_main(username=""):
   mydb = DataBase("root", "root", "localhost", "indusstock")
   manager = StorageManager.create(mydb, username)
   storage = manager.get_storage(mydb)


   def show_content(action):
       if action == "Store Orders":
           get_store_orders(content_frame, storage, mydb)
       if action == "Storage Orders":
           get_storage_orders(content_frame, storage, mydb)
       if action == "Staff":
           get_workers(content_frame, storage, mydb)
       if action == "Products":
           get_products(content_frame, storage, mydb)
       if action == "Stores":
           get_stores(content_frame, mydb)
       if action == "Go Back":
           starter_page(content_frame, manager.name, storage)


   window = tk.Tk()
   window.title("Storage Manager Page")
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


   button_texts = ["Store Orders", "Storage Orders", "Staff", "Products", "Stores", "Go Back"]
   for text in button_texts:
       btn = tk.Button(sidebar, text=text, width=15, pady=5, command=lambda t=text: show_content(t))
       btn.pack(pady=5)


   starter_page(content_frame, manager.name, storage)


   window.mainloop()
