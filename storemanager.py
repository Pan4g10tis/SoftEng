import csv
import tkinter as tk
from tkinter import ttk, messagebox , filedialog
from datetime import datetime, date, timedelta
from PIL import Image, ImageTk
import calendar
from classes import StoreManager,  StoreOrder, WorkerShift, DataBase , StoreSale


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


def get_sales(frame, store, mydb):
   for widget in frame.winfo_children():
       widget.destroy()

   def import_csv():
       file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
       if not file_path:
           return

       try:
           with open(file_path, newline='', encoding='utf-8') as csvfile:
               reader = csv.reader(csvfile)
               inserted_sales = 0

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

                   new_sale = StoreSale(
                       sale_id=None,
                       store=store.id,
                       date=datetime.today().date(),
                       products=products,
                       amounts=amounts
                   )
                   new_sale.insert_sale(mydb)
                   inserted_sales += 1

               messagebox.showinfo("Import Complete", f"{inserted_sales} sale(s) imported successfully.")
               nonlocal sales
               sales = store.show_sales(mydb)
               fetch_sales()

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

   sales = store.show_sales(mydb)

   def make_popup(sale_obj):
       def show_popup(event=None):
           popup = tk.Toplevel()
           popup.title(f"Sale #{sale_obj.id} Details")
           popup.geometry("400x300")
           popup.configure(bg="white")

           details = f"Order ID: {sale_obj.id}\nSale Date: {sale_obj.date}"

           msg = tk.Label(popup, text=details.strip(), justify="left", bg="white", font=("Arial", 12))
           msg.pack(padx=20, pady=20)

           product_frame = tk.Frame(popup, bg="white")
           product_frame.pack(padx=20, pady=10, anchor="w")

           tk.Label(product_frame, text="Products Sold:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")

           for product, amount in zip(sale_obj.products, sale_obj.amounts):
               line = f"• {product}: {amount}"
               tk.Label(product_frame, text=line, font=("Arial", 11), bg="white").pack(anchor="w")

           tk.Button(popup, text="Close", command=popup.destroy).pack(pady=20)

       return show_popup

   def fetch_sales():
       start = start_entry.get()
       end = end_entry.get()

       view_sales = sales

       if start:
           try:
               start_date = datetime.strptime(start, "%Y-%m-%d").date()
               view_sales = [s for s in view_sales if s.date >= start_date]
           except:
               pass
       if end:
           try:
               end_date = datetime.strptime(end, "%Y-%m-%d").date()
               view_sales = [s for s in view_sales if s.date <= end_date]
           except:
               pass

       for widget in list_frame.winfo_children():
           widget.destroy()

       headings = ["Order ID", "Sale Date"]
       for col, title in enumerate(headings):
           tk.Label(list_frame, text=title, font=("Arial", 12, "bold"), bg="white", borderwidth=1, relief="solid",
                    width=20).grid(row=0, column=col)

       for row, sale in enumerate(view_sales, start=1):
           label = tk.Label(list_frame, text=sale.id, bg="white", borderwidth=1, relief="solid", width=20,
                            cursor="hand2")
           label.grid(row=row, column=0)
           label.bind("<Button-1>", make_popup(sale))

           tk.Label(list_frame, text=str(sale.date), bg="white", borderwidth=1, relief="solid", width=20).grid(
               row=row, column=1)

   def export_csv():
       start = start_entry.get()
       end = end_entry.get()
       view_sales = sales

       if start:
           try:
               start_date = datetime.strptime(start, "%Y-%m-%d").date()
               view_sales = [s for s in view_sales if s.date >= start_date]
           except:
               pass
       if end:
           try:
               end_date = datetime.strptime(end, "%Y-%m-%d").date()
               view_sales = [s for s in view_sales if s.date <= end_date]
           except:
               pass

       if not view_sales:
           messagebox.showinfo("Export", "No sales to export.")
           return

       file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")])
       if not file_path:
           return

       try:
           with open(file_path, "w", newline='', encoding="utf-8") as csvfile:
               writer = csv.writer(csvfile)
               for sale in view_sales:
                   row = []
                   for p, a in zip(sale.products, sale.amounts):
                       row.extend([p, a])
                   writer.writerow(row)
           messagebox.showinfo("Export Complete", f"{len(view_sales)} sale(s) exported successfully.")
       except Exception as e:
           messagebox.showerror("Export Failed", f"Could not write to CSV:\n{e}")

   tk.Button(filter_frame, text="Search", command=fetch_sales).grid(row=0, column=6, padx=10)
   tk.Button(filter_frame, text="Export CSV", command=export_csv).grid(row=0, column=7, padx=10)

   list_frame = tk.Frame(frame, bg="white")
   list_frame.pack(pady=10, fill="both", expand=True)

   fetch_sales()

   
def get_products(frame, store, mydb):
   for widget in frame.winfo_children():
       widget.destroy()

   filter_frame = tk.Frame(frame, bg="white")
   filter_frame.pack(pady=10)

   products = store.show_products(mydb)

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
           popup.geometry("400x700")
           popup.configure(bg="white")

           details = (f"Product ID: {product_obj.id}\nName: {product_obj.name}\nManufacturer: "
                      f"{product_obj.manufacturer}\nType: {product_obj.type}\nPrice: {product_obj.price}"
                      f"\nStock: {product_obj.stock}")

           msg = tk.Label(popup, text=details.strip(), justify="left", bg="white", font=("Arial", 12))
           msg.pack(padx=20, pady=10)

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
                   sales = product_obj.store_sale_stats(mydb, store.id, start_date, end_date)
                   orders = product_obj.store_order_stats(mydb, store.id, start_date, end_date)
                   result_label.config(text=f"Total Units Sold: {sales}\nTotal Units Ordered: {orders}")
               except Exception as e:
                   result_label.config(text=f"Error: {e}")

           tk.Button(popup, text="Show Sales Stats", command=show_stats).pack(pady=5)

           tk.Label(popup, text="Add a Note:", bg="white", font=("Arial", 11, "bold")).pack(pady=(10, 0))
           note_text = tk.Text(popup, height=4, width=40)
           note_text.pack(pady=5)

           def submit_note():
               note_content = note_text.get("1.0", "end").strip()
               if note_content:
                   try:
                       product_obj.insert_notes(mydb, store.id, note_content)
                       note_text.delete("1.0", "end")
                       fetch_notes()
                   except Exception as e:
                       messagebox.showerror("Error", f"Failed to insert note:\n{e}")

           tk.Button(popup, text="Submit Note", command=submit_note).pack(pady=5)

           # Existing Notes Display
           notes_frame = tk.Frame(popup, bg="white")
           notes_frame.pack(fill="both", expand=True, padx=10, pady=10)

           notes_label = tk.Label(notes_frame, text="Existing Notes:", bg="white", font=("Arial", 11, "bold"))
           notes_label.pack(anchor="w")

           notes_display = tk.Text(notes_frame, height=10, width=45, state="disabled", wrap="word", bg="#f5f5f5")
           notes_display.pack(fill="both", expand=True)


           def fetch_notes():
               try:
                   notes = product_obj.show_notes(mydb, store.id)
                   notes_display.config(state="normal")
                   notes_display.delete("1.0", "end")
                   if notes:
                       for n in notes:
                           notes_display.insert("end", f"- {n}\n")
                   else:
                       notes_display.insert("end", "No notes available.")
                   notes_display.config(state="disabled")
               except Exception as e:
                   notes_display.config(state="normal")
                   notes_display.delete("1.0", "end")
                   notes_display.insert("end", f"Error loading notes: {e}")
                   notes_display.config(state="disabled")

           # Initial notes load
           fetch_notes()

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


def get_workers(frame, store, mydb):
   for widget in frame.winfo_children():
       widget.destroy()

   workers = store.show_workers(mydb)

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
                    shift.insert_store_shift(mydb)
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
