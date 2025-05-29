import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import calendar
from datetime import datetime, date, timedelta
from PIL import Image, ImageTk
from classes import StorageManager, Store, WorkerShift, DataBase, Product, StorageOrder


def starter_page(frame, name, storage):
   for widget in frame.winfo_children():
       widget.destroy()


   starter_text = (f"Welcome {name}!\nStorage Info:\nAddress: {storage.address}\nEmail: {storage.email}\n"
                   f"Phone: {storage.phone}")
   starter_label = tk.Label(frame, text=starter_text, font=("Arial", 16), bg="white", justify="left")
   starter_label.pack(pady=10)

def get_storage_orders(frame, storage, mydb):
   for widget in frame.winfo_children():
       widget.destroy()


   def import_csv():
       file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
       if not file_path:
           return


       try:
           with open(file_path, newline='', encoding='utf-8') as csvfile:
               reader = csv.reader(csvfile)
               imported = 0


               for row in reader:
                   products = []
                   amounts = []


                   for i in range(0, len(row), 2):
                       try:
                           product = row[i].strip()
                           amount = float(row[i + 1].strip())
                           products.append(product)
                           amounts.append(amount)
                       except (IndexError, ValueError):
                           continue


                   if not products:
                       continue


                   new_order = StorageOrder(
                       order_id=None,
                       status='PENDING',
                       start_date=datetime.today().date(),
                       end_date=None,
                       products=products,
                       amounts=amounts
                   )
                   new_order.insert_order(mydb)
                   imported += 1


               messagebox.showinfo("Import Complete", f"{imported} order(s) imported successfully.")
               nonlocal orders
               orders = storage.show_storage_orders(mydb)
               fetch_orders()


       except Exception as e:
           messagebox.showerror("Import Failed", f"Could not import CSV: {e}")


   import_button = tk.Button(frame, text="Import CSV", command=import_csv)
   import_button.pack(pady=(10, 0))


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
   status_combobox['values'] = ["ALL", "PENDING", "COMPLETED", "CANCELED"]
   status_combobox.current(0)
   status_combobox.grid(row=0, column=5, padx=5)


   orders = storage.show_storage_orders(mydb)


   def make_popup(order_obj):
       def show_popup(event=None):
           popup = tk.Toplevel()
           popup.title(f"Order #{order_obj.id} Details")
           popup.geometry("400x300")
           popup.configure(bg="white")


           details = (f"Order ID: {order_obj.id}\nStatus: {order_obj.status}\nStart Date: {order_obj.start_date}\n"
                      f"End Date: {order_obj.end_date}\n")


           msg = tk.Label(popup, text=details.strip(), justify="left", bg="white", font=("Arial", 12))
           msg.pack(padx=20, pady=20)


           if order_obj.status.upper() == "PENDING":
               btn_frame = tk.Frame(popup, bg="white")
               btn_frame.pack(pady=(0, 10))


               def mark_complete():
                   order_obj.complete_order(mydb)
                   popup.destroy()
                   nonlocal orders
                   orders = storage.show_storage_orders(mydb)
                   fetch_orders()


               def mark_canceled():
                   order_obj.cancel_order(mydb)
                   popup.destroy()
                   nonlocal orders
                   orders = storage.show_storage_orders(mydb)
                   fetch_orders()


               tk.Button(btn_frame, text="Complete", bg="white", fg="black", width=10, command=mark_complete).pack(
                   side="left", padx=10)
               tk.Button(btn_frame, text="Cancel", bg="white", fg="black", width=10, command=mark_canceled).pack(
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


def get_products(frame, storage, mydb):
   for widget in frame.winfo_children():
       widget.destroy()


   def open_new_product_popup():
       popup = tk.Toplevel()
       popup.title("Add New Product")
       popup.geometry("300x450")
       popup.configure(bg="white")


       tk.Label(popup, text="Name:", bg="white").pack(pady=5)
       name_entry = tk.Entry(popup)
       name_entry.pack(pady=5)


       tk.Label(popup, text="Manufacturer:", bg="white").pack(pady=5)
       manu_entry = tk.Entry(popup)
       manu_entry.pack(pady=5)


       tk.Label(popup, text="Type:", bg="white").pack(pady=5)
       type_entry = tk.Entry(popup)
       type_entry.pack(pady=5)


       tk.Label(popup, text="Price:", bg="white").pack(pady=5)
       price_entry = tk.Entry(popup)
       price_entry.pack(pady=5)


       result_label = tk.Label(popup, text="", bg="white", fg="red")
       result_label.pack(pady=10)


       def submit_product():
           name = name_entry.get().strip()
           manu = manu_entry.get().strip()
           type = type_entry.get().strip().upper()
           try:
   	         price = float(price_entry.get().strip())
   		   if price <= 0:
                   result_label.config(text="Price must be greater than 0.")
                   return		   
           except ValueError:
               result_label.config(text="Invalid price.")
               return


           if not name or not manu:
               result_label.config(text="All fields are required.")
               return


           product = Product(0, name, manu, type, price,0)


           try:
               product.insert_product(mydb)
               popup.destroy()
               nonlocal products
               products = storage.show_products(mydb)
               fetch_products()
           except Exception as e:
               result_label.config(text=f"Error: {e}")


       tk.Button(popup, text="Submit", command=submit_product).pack(pady=10)
       tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5)


   tk.Button(frame, text="Add New Product", command=open_new_product_popup).pack(pady=5)


   filter_frame = tk.Frame(frame, bg="white")
   filter_frame.pack(pady=10)




   products = storage.show_products(mydb)


   tk.Label(filter_frame, text="Type:", bg="white").grid(row=0, column=4, padx=5, pady=5)
   type_var = tk.StringVar()
   type_combobox = ttk.Combobox(filter_frame, textvariable=type_var)
   product_types = sorted(set([p.type.upper() for p in products]))
   type_combobox['values'] = ["ALL"] + product_types
   type_combobox.current(0)
   type_combobox.grid(row=0, column=5, padx=5)


   def make_popup(product_obj):
       def show_popup(event=None):
           popup = tk.Toplevel()
           popup.title(f"Product #{product_obj.id} Details")
           popup.geometry("400x450")
           popup.configure(bg="white")


           details = (f"Product ID: {product_obj.id}\nName: {product_obj.name}\nManufacturer: "
                      f"{product_obj.manufacturer}\nType: {product_obj.type}\nPrice: {product_obj.price}"
                      f"\nStock: {product_obj.stock}")


           msg = tk.Label(popup, text=details.strip(), justify="left", bg="white", font=("Arial", 12))
           msg.pack(padx=20, pady=10)


           def delete_product():
               try:
                   product_obj.delete_product(mydb)
                   popup.destroy()
                   nonlocal products
                   products = storage.show_products(mydb)
                   fetch_products()
               except Exception as e:
                   result_label.config(text=f"Error deleting product: {e}", fg="red")


           tk.Button(popup, text="Delete Product", command=delete_product, bg="red", fg="white").pack(pady=5)


           date_frame = tk.Frame(popup, bg="white")
           date_frame.pack(pady=10)


           tk.Label(date_frame, text="Start Date (YYYY-MM-DD):", bg="white").grid(row=0, column=0, padx=5, pady=5)
           start_entry = tk.Entry(date_frame)
           start_entry.grid(row=0, column=1, padx=5, pady=5)


           tk.Label(date_frame, text="End Date (YYYY-MM-DD):", bg="white").grid(row=1, column=0, padx=5, pady=5)
           end_entry = tk.Entry(date_frame)
           end_entry.grid(row=1, column=1, padx=5, pady=5)


           result_label = tk.Label(popup, text="", bg="white", font=("Arial", 11))
           result_label.pack(pady=10)


           def show_stats():
               start = start_entry.get().strip()
               end = end_entry.get().strip()


               try:
                   start_date = datetime.strptime(start, "%Y-%m-%d").date()
               except:
                   start_date = date(1, 1, 1)  # "0001-01-01"


               try:
                   end_date = datetime.strptime(end, "%Y-%m-%d").date()
               except:
                   end_date = date(9999, 12, 31)  # "9999-12-31"


               try:
                   sent = product_obj.storage_sent_stats(mydb, storage.id, start_date, end_date)
                   orders = product_obj.storage_order_stats(mydb, storage.id, start_date, end_date)
                   result_label.config(text=f"Total Units Sent: {sent}\nTotal Units Ordered: {orders}")
               except Exception as e:
                   result_label.config(text=f"Error: {e}")


           tk.Button(popup, text="Show Sales Stats", command=show_stats).pack(pady=5)


           tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)


       return show_popup


   def fetch_products():
       prod_type = type_var.get()


       view_products = products


       if prod_type != "ALL":
           view_products = [p for p in view_products if p.type == prod_type]


       for widget in list_frame.winfo_children():
           widget.destroy()


       headings = ["Product ID", "Name", "Stock"]
       for col, title in enumerate(headings):
           tk.Label(list_frame, text=title, font=("Arial", 12, "bold"), bg="white", borderwidth=1, relief="solid",
                    width=20).grid(row=0, column=col)


       for row, product in enumerate(view_products, start=1):
           label = tk.Label(list_frame, text=product.id, bg="white", borderwidth=1, relief="solid", width=20,
                            cursor="hand2")
           label.grid(row=row, column=0)
           label.bind("<Button-1>", make_popup(product))


           tk.Label(list_frame, text=product.name, bg="white", borderwidth=1, relief="solid", width=30).grid(row=row,
                                                                                                             column=1)
           tk.Label(list_frame, text=str(product.stock), bg="white", borderwidth=1, relief="solid", width=20).grid(
               row=row, column=2)


   tk.Button(filter_frame, text="Search", command=fetch_products).grid(row=0, column=6, padx=10)


   list_frame = tk.Frame(frame, bg="white")
   list_frame.pack(pady=10, fill="both", expand=True)


   fetch_products()



def get_workers(frame, storage, mydb):
   for widget in frame.winfo_children():
       widget.destroy()


   workers = storage.show_workers(mydb)


   list_frame = tk.Frame(frame, bg="white")
   list_frame.pack(pady=10, fill="both", expand=True)


   def make_popup(worker_obj):
       def show_popup(event=None):
           popup = tk.Toplevel()
           popup.title(f"{worker_obj.surname} Details")
           popup.geometry("400x500")
           popup.configure(bg="white")


           details = (f"Name: {worker_obj.name}\nSurname: {worker_obj.surname}\nEmail: {worker_obj.email}\n"
                      f"Phone: {worker_obj.phone}")
           msg = tk.Label(popup, text=details.strip(), justify="left", bg="white", font=("Arial", 12))
           msg.pack(padx=20, pady=10)


           form_frame = tk.Frame(popup, bg="white")
           form_frame.pack(pady=10)


           tk.Label(form_frame, text="Shift Date (YYYY-MM-DD):", bg="white").grid(row=0, column=0, sticky="w")
           date_entry = tk.Entry(form_frame)
           date_entry.grid(row=0, column=1)


           tk.Label(form_frame, text="Start Time (HH:MM):", bg="white").grid(row=1, column=0, sticky="w")
           start_entry = tk.Entry(form_frame)
           start_entry.grid(row=1, column=1)


           tk.Label(form_frame, text="End Time (HH:MM):", bg="white").grid(row=2, column=0, sticky="w")
           end_entry = tk.Entry(form_frame)
           end_entry.grid(row=2, column=1)


           def submit_shift():
                date = date_entry.get()
                start = start_entry.get()
                end = end_entry.get()

                if not (date and start and end):
                    messagebox.showerror("Error", "All fields must be filled.")
                    return

                try:
                    # Validate date format
                    datetime.strptime(date, "%Y-%m-%d")

                    # Parse start and end times into datetime objects for comparison
                    start_time = datetime.strptime(start, "%H:%M")
                    end_time = datetime.strptime(end, "%H:%M")

                    # Check that end time is after start time
                    if end_time <= start_time:
                        messagebox.showerror("Error", "End time must be after start time.")
                        return

                except ValueError:
                    messagebox.showerror(
                        "Error",
                        "Invalid date or time format.\nExpected formats:\nDate: YYYY-MM-DD\nTime: HH:MM"
                    )
                    return

                try:
                    shift = WorkerShift(worker_obj.id, date, start, end)
                    shift.insert_storage_shift(mydb)
                    messagebox.showinfo("Success", "Shift added successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add shift: {e}")


           tk.Button(popup, text="Add Shift", command=submit_shift).pack(pady=10)


           tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)


       return show_popup


   headings = ["Name", "Surname"]
   for col, title in enumerate(headings):
       tk.Label(list_frame, text=title, font=("Arial", 12, "bold"), bg="white", borderwidth=1, relief="solid",
                width=20).grid(row=0, column=col)


   for row, worker in enumerate(workers, start=1):
       label = tk.Label(list_frame, text=worker.name, bg="white", borderwidth=1, relief="solid", width=20,
                        cursor="hand2")
       label.grid(row=row, column=0)
       label.bind("<Button-1>", make_popup(worker))


       tk.Label(list_frame, text=worker.surname, bg="white", borderwidth=1, relief="solid", width=20).grid(row=row,
                                                                                                         column=1)


   calendar_frame = tk.Frame(frame, bg="white")
   calendar_frame.pack(pady=10)


   shift_display_frame = tk.Frame(frame, bg="white")
   shift_display_frame.pack(pady=10, fill="both", expand=True)


   current_date = datetime.today()


   def render_calendar(year, month):
       for widget in calendar_frame.winfo_children():
           widget.destroy()


       nav_frame = tk.Frame(calendar_frame, bg="white")
       nav_frame.pack()


       def go_prev():
           nonlocal current_date
           prev_month = current_date.replace(day=1) - timedelta(days=1)
           current_date = prev_month
           render_calendar(current_date.year, current_date.month)


       def go_next():
           nonlocal current_date
           next_month = current_date.replace(day=28) + timedelta(days=4)  # Always lands in next month
           current_date = next_month.replace(day=1)
           render_calendar(current_date.year, current_date.month)


       tk.Button(nav_frame, text="<", command=go_prev).pack(side="left", padx=10)
       tk.Label(nav_frame, text=f"{calendar.month_name[month]} {year}", font=("Arial", 14, "bold"),
                bg="white").pack(side="left", padx=10)
       tk.Button(nav_frame, text=">", command=go_next).pack(side="left", padx=10)


       # Days of the week
       days_frame = tk.Frame(calendar_frame, bg="white")
       days_frame.pack()
       for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
           tk.Label(days_frame, text=day, bg="white", font=("Arial", 10, "bold"), width=5).grid(row=0, column=i)


       # Calendar days
       cal = calendar.monthcalendar(year, month)
       for row_idx, week in enumerate(cal, start=1):
           for col_idx, day in enumerate(week):
               if day == 0:
                   continue
               date_str = f"{year}-{month:02d}-{day:02d}"
               tk.Button(days_frame, text=str(day), width=5,
                         command=lambda d=date_str: on_date_click(d)).grid(row=row_idx, column=col_idx, padx=1, pady=1)


   def on_date_click(date_str):
       for widget in shift_display_frame.winfo_children():
           widget.destroy()


       tk.Label(shift_display_frame, text=f"Shifts on {date_str}",
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=(0, 5))


       shift_found = False
       for worker in workers:
           shifts = worker.show_store_shift(mydb, date_str)
           for surname, start, end in shifts:
               shift_found = True
               text = f"{surname}: {start} - {end}"
               tk.Label(shift_display_frame, text=text, bg="white", font=("Arial", 11)).pack(anchor="w", padx=20,
                                                                                             pady=2)


       if not shift_found:
           tk.Label(shift_display_frame, text="No shifts for this date.",
                    bg="white", font=("Arial", 11, "italic")).pack(anchor="w", padx=20, pady=5)


   # Initial calendar render
   render_calendar(current_date.year, current_date.month)




def get_stores(frame, mydb):
   for widget in frame.winfo_children():
       widget.destroy()


   list_frame = tk.Frame(frame, bg="white")
   list_frame.pack(pady=10, fill="both", expand=True)


   conn = mydb.connect_db()
   cursor = conn.cursor()
   cursor.execute("SELECT id, address, email, phone FROM store")
   rows = cursor.fetchall()
   stores=[]
   for row in rows:
       store = Store(*row)
       stores.append(store)
   conn.close()


   def make_popup(store_obj):
       def show_popup(event=None):
           popup = tk.Toplevel()
           popup.title(f"Store #{store_obj.id} Details")
           popup.geometry("400x450")
           popup.configure(bg="white")


           details = (f"Store ID: {store_obj.id}\nAddress: {store_obj.address}\n"
                      f"Email: {store_obj.email}\nPhone: {store_obj.phone}")


           msg = tk.Label(popup, text=details.strip(), justify="left", bg="white", font=("Arial", 12))
           msg.pack(padx=20, pady=10)


           # Date range inputs
           date_frame = tk.Frame(popup, bg="white")
           date_frame.pack(pady=10)


           tk.Label(date_frame, text="Start Date (YYYY-MM-DD):", bg="white").grid(row=0, column=0, padx=5, pady=5)
           start_entry = tk.Entry(date_frame)
           start_entry.grid(row=0, column=1, padx=5, pady=5)


           tk.Label(date_frame, text="End Date (YYYY-MM-DD):", bg="white").grid(row=1, column=0, padx=5, pady=5)
           end_entry = tk.Entry(date_frame)
           end_entry.grid(row=1, column=1, padx=5, pady=5)


           result_label = tk.Label(popup, text="", bg="white", font=("Arial", 11))
           result_label.pack(pady=10)


           def show_stats():
               start = start_entry.get().strip()
               end = end_entry.get().strip()


               try:
                   start_date = datetime.strptime(start, "%Y-%m-%d").date()
               except:
                   start_date = date(1, 1, 1)  # Fallback start


               try:
                   end_date = datetime.strptime(end, "%Y-%m-%d").date()
               except:
                   end_date = date(9999, 12, 31)  # Fallback end


               try:
                   orders = store_obj.show_stats(mydb, start_date, end_date)
                   result_label.config(text=f"Total Orders: {orders}")
               except Exception as e:
                   result_label.config(text=f"Error: {e}")


           tk.Button(popup, text="Show Store Stats", command=show_stats).pack(pady=5)
           tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)


       return show_popup


   headings = ["ID", "Address"]
   for col, title in enumerate(headings):
       tk.Label(list_frame, text=title, font=("Arial", 12, "bold"), bg="white", borderwidth=1, relief="solid",
                width=20).grid(row=0, column=col)


   for row, store in enumerate(stores, start=1):
       label = tk.Label(list_frame, text=store.id, bg="white", borderwidth=1, relief="solid", width=20,
                        cursor="hand2")
       label.grid(row=row, column=0)
       label.bind("<Button-1>", make_popup(store))


       tk.Label(list_frame, text=store.address, bg="white", borderwidth=1, relief="solid", width=20).grid(row=row,
                                                                                                         column=1)


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
