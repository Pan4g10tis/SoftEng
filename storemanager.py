import tkinter as tk
from PIL import Image, ImageTk
from classes import StoreManager,DataBase
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from classes import StoreOrder




def starter_page(frame, name, store):
   for widget in frame.winfo_children():
       widget.destroy()


   starter_text = f"""Welcome {name}!\nStore Info:\nAddress: {store.address}\nEmail: {store.email}\nPhone: {store.phone}"""
   starter_label = tk.Label(frame, text=starter_text, font=("Arial", 16), bg="white", justify="left")
   starter_label.pack(pady=10)



def get_orders(frame, store, mydb):
   for widget in frame.winfo_children():
       widget.destroy()


   def open_new_order_popup():
       popup = tk.Toplevel()
       popup.title("Create New Order")
       popup.geometry("700x600")
       popup.configure(bg="white")


       # Priority selection
       priority_var = tk.StringVar(value="NORMAL")
       priority_frame = tk.Frame(popup, bg="white")
       priority_frame.pack(pady=10)


       tk.Label(priority_frame, text="Priority:", bg="white").pack(side="left", padx=5)
       tk.Radiobutton(priority_frame, text="Normal", variable=priority_var, value="NORMAL", bg="white").pack(
           side="left", padx=5)
       tk.Radiobutton(priority_frame, text="High", variable=priority_var, value="HIGH", bg="white").pack(side="left",
                                                                                                         padx=5)


       filter_frame = tk.Frame(popup, bg="white")
       filter_frame.pack(pady=10)


       tk.Label(filter_frame, text="Type:", bg="white").grid(row=0, column=0, padx=5)
       type_var = tk.StringVar()
       type_combobox = ttk.Combobox(filter_frame, textvariable=type_var)
       type_combobox['values'] = ["ALL", "BOLT", "NUT", "PIPE", "TOOLS"]
       type_combobox.current(0)
       type_combobox.grid(row=0, column=1, padx=5)


       product_list_frame = tk.Frame(popup, bg="white")
       product_list_frame.pack(pady=10, fill="both", expand=True)


       selected_products = {}


       def fetch_products():
           for widget in product_list_frame.winfo_children():
               widget.destroy()


           products = store.show_products(mydb)
           filtered = products
           if type_var.get() != "ALL":
               filtered = [p for p in products if p.type == type_var.get()]


           headings = ["ID", "Name", "Order Amount"]
           for col, title in enumerate(headings):
               tk.Label(product_list_frame, text=title, font=("Arial", 12, "bold"), bg="white",
                        borderwidth=1, relief="solid", width=20).grid(row=0, column=col)


           for row, product in enumerate(filtered, start=1):
               tk.Label(product_list_frame, text=product.id, bg="white", borderwidth=1, relief="solid", width=20).grid(
                   row=row, column=0)
               tk.Label(product_list_frame, text=product.name, bg="white", borderwidth=1, relief="solid",
                        width=30).grid(row=row, column=1)


               amount_var = tk.StringVar()
               tk.Entry(product_list_frame, textvariable=amount_var, width=10).grid(row=row, column=2)
               selected_products[product] = amount_var


       tk.Button(filter_frame, text="Search", command=fetch_products).grid(row=0, column=2, padx=10)
       fetch_products()


       def submit_order():
           priority = priority_var.get()


           products = []
           amounts = []


           for product, var in selected_products.items():
               try:
                   amt = int(var.get())
                   if amt > 0:
                       products.append(product.id)
                       amounts.append(amt)
               except:
                   continue


           if priority == "HIGH" and len(products) > 3:
               tk.messagebox.showerror("Limit Exceeded", "High priority orders can only include up to 3 products.")
               return


           if products:
               order = StoreOrder(0, store.id, priority, 'PENDING', 0, 0, products, amounts)
               order.insert_order(mydb)
               popup.destroy()
               nonlocal orders
               orders = store.show_orders(mydb)
               fetch_orders()


       tk.Button(popup, text="Submit Order", bg="green", fg="white", command=submit_order).pack(pady=10)
       tk.Button(popup, text="Close", command=popup.destroy).pack(pady=5)


   # Top bar with New Order button
   top_btn_frame = tk.Frame(frame, bg="white")
   top_btn_frame.pack(pady=(10, 0))
   tk.Button(top_btn_frame, text="New Order", command=open_new_order_popup, bg="blue", fg="white").pack()


   filter_frame = tk.Frame(frame, bg="white")
   filter_frame.pack(pady=10)


   tk.Label(filter_frame, text="Date: From: (YYYY-MM-DD):", bg="white").grid(row=0, column=0, padx=5, pady=5)
   start_entry = tk.Entry(filter_frame)
   start_entry.grid(row=0, column=1, padx=5)


   tk.Label(filter_frame, text="To: (YYYY-MM-DD):", bg="white").grid(row=0, column=2, padx=5, pady=5)
   end_entry = tk.Entry(filter_frame)
   end_entry.grid(row=0, column=3, padx=5)


   tk.Label(filter_frame, text="Status:", bg="white").grid(row=0, column=4, padx=5, pady=5)
   status_var = tk.StringVar()
   status_combobox = ttk.Combobox(filter_frame, textvariable=status_var)
   status_combobox['values'] = ["ALL", "PENDING", "CONFIRMED", "SENT", "COMPLETED", "CANCELED"]
   status_combobox.current(0)
   status_combobox.grid(row=0, column=5, padx=5)


   orders = store.show_orders(mydb)


   def make_popup(order_obj):
       def show_popup(event=None):
           popup = tk.Toplevel()
           popup.title(f"Order #{order_obj.id} Details")
           popup.geometry("400x300")
           popup.configure(bg="white")


           details = (f"Order ID: {order_obj.id}\nStatus: {order_obj.status}\nPriority: {order_obj.priority}\n"
                      f"Start Date: {order_obj.start_date}\nEnd Date: {order_obj.end_date}\n")


           msg = tk.Label(popup, text=details.strip(), justify="left", bg="white", font=("Arial", 12))
           msg.pack(padx=20, pady=20)


           btn_frame = tk.Frame(popup, bg="white")
           btn_frame.pack(pady=(0, 10))


           if order_obj.status.upper() == "PENDING":


               def mark_canceled():
                   order_obj.cancel_order(mydb)
                   popup.destroy()
                   nonlocal orders
                   orders = store.show_orders(mydb)
                   fetch_orders()


               tk.Button(btn_frame, text="Cancel", bg="white", fg="black", width=10, command=mark_canceled).pack(
                   side="left", padx=10)


           if order_obj.status.upper() == "SENT":


               def mark_complete():
                   order_obj.complete_order(mydb)
                   popup.destroy()
                   nonlocal orders
                   orders = store.show_orders(mydb)
                   fetch_orders()


               tk.Button(btn_frame, text="Complete", bg="white", fg="black", width=10, command=mark_complete).pack(
                   side="left", padx=10)


           product_frame = tk.Frame(popup, bg="white")
           product_frame.pack(padx=20, pady=10, anchor="w")


           tk.Label(product_frame, text="Products Ordered:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")


           for product, amount in zip(order_obj.products, order_obj.amounts):
               line = f"• {product}: {amount}"
               tk.Label(product_frame, text=line, font=("Arial", 11), bg="white").pack(anchor="w")


           tk.Button(popup, text="Close", command=popup.destroy).pack(pady=20)


       return show_popup


   def fetch_orders():
       start = start_entry.get()
       end = end_entry.get()
       status = status_var.get()


       view_orders = orders


       if start:
           try:
               start_date = datetime.strptime(start, "%Y-%m-%d").date()
               view_orders = [o for o in view_orders if o.start_date >= start_date]
           except:
               pass
       if end:
           try:
               end_date = datetime.strptime(end, "%Y-%m-%d").date()
               view_orders = [o for o in view_orders if o.start_date <= end_date]
           except:
               pass
       if status != "ALL":
           view_orders = [o for o in view_orders if o.status == status]


       for widget in list_frame.winfo_children():
           widget.destroy()


       headings = ["Order ID", "Status", "Start Date"]
       for col, title in enumerate(headings):
           tk.Label(list_frame, text=title, font=("Arial", 12, "bold"), bg="white", borderwidth=1, relief="solid",
                    width=20).grid(row=0, column=col)


       for row, order in enumerate(view_orders, start=1):
           label = tk.Label(list_frame, text=order.id, bg="white", borderwidth=1, relief="solid", width=20,
                            cursor="hand2")
           label.grid(row=row, column=0)
           label.bind("<Button-1>", make_popup(order))


           tk.Label(list_frame, text=order.status, bg="white", borderwidth=1, relief="solid", width=20).grid(row=row,
                                                                                                             column=1)
           tk.Label(list_frame, text=str(order.start_date), bg="white", borderwidth=1, relief="solid", width=20).grid(
               row=row, column=2)


   tk.Button(filter_frame, text="Search", command=fetch_orders).grid(row=0, column=6, padx=10)


   list_frame = tk.Frame(frame, bg="white")
   list_frame.pack(pady=10, fill="both", expand=True)


   fetch_orders()





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


