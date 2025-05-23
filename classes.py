Mnimport mysql.connector




class DataBase:
   def __init__(self, user, password, host, database):
       self.user = user
       self.password = password
       self.host = host
       self.database = database


   def connect_db(self):
       return mysql.connector.connect(
           user=self.user,
           password=self.password,
           host=self.host,
           database=self.database
       )salStoreSa




class Store:
   def __init__(self, store_id, address, email, phone):
       self.id = store_id
       self.address = address
       self.email = email
       self.phone = phone


   def show_orders(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, priority, status, start_date, end_date FROM store_order WHERE store = %s",
                      (self.id,))
       rows = cursor.fetchall()
       orders = []
       for row in rows:
           order = StoreOrder(row[0], self.id, row[1], row[2], row[3], row[4], [], [])
           cursor.execute("SELECT product,amount FROM store_order_product WHERE order_num = %s",
                          (order.id,))
           prod_rows = cursor.fetchall()
           for prod_row in prod_rows:
               order.products.append(prod_row[0])
               order.amounts.append(prod_row[1])
           orders.append(order)
       conn.close()
       return orders


   def show_sales(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, sale_date FROM store_sale WHERE store = %s",
                      (self.id,))
       rows = cursor.fetchall()
       sales = []
       for row in rows:
           sale = StoreSale(row[0], self.id, row[1], [], [])
           cursor.execute("SELECT product,amount FROM store_sale_product WHERE sale_num = %s",
                          (sale.id,))
           prod_rows = cursor.fetchall()
           for prod_row in prod_rows:
               sale.products.append(prod_row[0])
               sale.amounts.append(prod_row[1])
           sales.append(sale)
       conn.close()
       return sales


   def show_workers(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, name, surname, email, phone FROM store_worker WHERE store = %s", (self.id,))
       rows = cursor.fetchall()
       workers = []
       for row in rows:
           worker = Worker(*row)
           workers.append(worker)
       conn.close()
       return workers


   def show_products(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, name, manufacturer, type, price, stock "
                      "FROM product INNER JOIN product_store_stock ON product.id = product_store_stock.product "
                      "WHERE store = %s", (self.id,))
       rows = cursor.fetchall()
       products = []
       for row in rows:
           product = Product(*row)
           products.append(product)
       conn.close()
       return products


   def show_stats(self, mydb, start_date, end_date):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT COUNT(id) from store_order WHERE store = %s AND start_date BETWEEN %s AND %s",
                      (self.id,start_date,end_date))
       result = cursor.fetchone()
       return result[0]




class Storage:
   def __init__(self, storage_id, address, email, phone):
       self.id = storage_id
       self.address = address
       self.email = email
       self.phone = phone


   def show_store_orders(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, store, priority, status, start_date, end_date FROM store_order WHERE storage = %s",
                      (self.id,))
       rows = cursor.fetchall()
       orders = []
       for row in rows:
           order = StoreOrder(row[0], row[1], row[2], row[3], row[4], row[5], [], [])
           cursor.execute("SELECT product,amount FROM store_order_product WHERE order_num = %s",
                          (order.id,))
           prod_rows = cursor.fetchall()
           for prod_row in prod_rows:
               order.products.append(prod_row[0])
               order.amounts.append(prod_row[1])
           orders.append(order)
       conn.close()
       return orders


   def show_storage_orders(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, status, start_date, end_date FROM storage_order WHERE storage = %s",
                      (self.id,))
       rows = cursor.fetchall()
       orders = []
       for row in rows:
           order = StorageOrder(row[0], row[1], row[2], row[3], [], [])
           cursor.execute("SELECT product,amount FROM storage_order_product WHERE order_num = %s",
                          (order.id,))
           prod_rows = cursor.fetchall()
           for prod_row in prod_rows:
               order.products.append(prod_row[0])
               order.amounts.append(prod_row[1])
           orders.append(order)
       conn.close()
       return orders


   def show_workers(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, name, surname, email, phone FROM storage_worker WHERE storage = %s", (self.id,))
       rows = cursor.fetchall()
       workers = []
       for row in rows:
           worker = Worker(*row)
           workers.append(worker)
       conn.close()
       return workers


   def show_products(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, name, manufacturer, type, price, stock "
                      "FROM product INNER JOIN product_storage_stock ON product.id = product_storage_stock.product "
                      "WHERE storage = %s", (self.id,))
       rows = cursor.fetchall()
       products = []
       for row in rows:
           product = Product(*row)
           products.append(product)
       conn.close()
       return products




class Worker:
   def __init__(self, worker_id, name, surname, email, phone):
       self.id = worker_id
       self.name = name
       self.surname = surname
       self.email = email
       self.phone = phone


   def show_store_shift(self, mydb, date):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT start_time, end_time FROM store_worker_shift "
                      "WHERE worker = %s AND shift_date = %s", (self.id, date))
       results = cursor.fetchall()
       return [(self.surname, start, end) for start, end in results]


   def show_storage_shift(self, mydb, date):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT start_time, end_time FROM storage_worker_shift "
                      "WHERE worker = %s AND shift_date = %s", (self.id, date))
       results = cursor.fetchall()
       return [(self.surname, start, end) for start, end in results]




class StoreManager:
   def __init__(self, username, password, name, surname, email, phone, store):
       self.username = username
       self.password = password
       self.name = name
       self.surname = surname
       self.email = email
       self.phone = phone
       self.store = store


   def get_store(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, address, email, phone FROM store INNER JOIN store_manager "
                      "ON store.id = store_manager.store WHERE username = %s", (self.username,))
       result = cursor.fetchone()
       conn.close()
       my_store = Store(*result)
       return my_store


   @classmethod
   def create(cls, mydb, username):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT manager.username, password, name, surname, email, phone, store"
                      " FROM manager INNER JOIN store_manager ON manager.username = store_manager.username"
                      " WHERE manager.username = %s", (username,))
       result = cursor.fetchone()
       manager = StoreManager(*result)
       return manager




class StorageManager:
   def __init__(self, username, password, name, surname, email, phone, storage):
       self.username = username
       self.password = password
       self.name = name
       self.surname = surname
       self.email = email
       self.phone = phone
       self.storage = storage


   def get_storage(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT id, address, email, phone FROM storage INNER JOIN storage_manager "
                      "ON storage.id = storage_manager.storage WHERE username = %s", (self.username,))
       result = cursor.fetchone()
       conn.close()
       my_storage = Storage(*result)
       return my_storage


   @classmethod
   def create(cls, mydb, username):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT manager.username, password, name, surname, email, phone, storage "
                      "FROM manager INNER JOIN storage_manager On manager.username = storage_manager.username "
                      "WHERE manager.username = %s", (username,))
       result = cursor.fetchone()
       manager = StorageManager(*result)
       return manager




class Product:
   def __init__(self, product_id, name, manufacturer, prod_type, price, stock):
       self.id = product_id
       self.name = name
       self.manufacturer = manufacturer
       self.type = prod_type
       self.price = price
       self.stock = stock


   def store_sale_stats(self, mydb, store, start_date, end_date):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT amount FROM store_sale_product "
                      "INNER JOIN store_sale ON store_sale_product.sale_num = store_sale.id "
                      "WHERE product = %s AND store_sale.store = %s "
                      "AND store_sale.sale_date BETWEEN %s AND %s", (self.id, store, start_date, end_date))
       rows = cursor.fetchall()
       conn.close()
       return sum(row[0] for row in rows)


   def store_order_stats(self, mydb, store, start_date, end_date):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT amount FROM store_order_product "
                      "INNER JOIN store_order ON store_order_product.order_num = store_order.id "
                      "WHERE product = %s AND store_order.store = %s "
                      "AND store_order.start_date BETWEEN %s AND %s", (self.id, store, start_date, end_date))
       rows = cursor.fetchall()
       conn.close()
       return sum(row[0] for row in rows)


   def storage_sent_stats(self, mydb, storage, start_date, end_date):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT amount FROM store_order_product "
                      "INNER JOIN store_order ON store_order_product.order_num = store_order.id "
                      "WHERE product = %s AND store_order.storage = %s "
                      "AND store_order.start_date BETWEEN %s AND %s", (self.id, storage, start_date, end_date))
       rows = cursor.fetchall()
       conn.close()
       return sum(row[0] for row in rows)


   def storage_order_stats(self, mydb, storage, start_date, end_date):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT amount FROM storage_order_product "
                      "INNER JOIN storage_order ON storage_order_product.order_num = storage_order.id "
                      "WHERE product = %s AND storage_order.storage = %s "
                      "AND storage_order.start_date BETWEEN %s AND %s", (self.id, storage, start_date, end_date))
       rows = cursor.fetchall()
       conn.close()
       return sum(row[0] for row in rows)


   def insert_product(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("INSERT INTO product(name,manufacturer,type,price) VALUES (%s, %s, %s, %s)",
                      (self.name, self.manufacturer, self.type, self.price))
       cursor.execute("SELECT MAX(id) FROM product")
       result = cursor.fetchone()
       self.id = result[0]
       try:
           cursor.execute("INSERT INTO product_store_stock VALUES (%s, 1, 0),(%s, 1, 0)",
                          (self.id, self.id))
           cursor.execute("INSERT INTO product_storage_stock VALUES (%s, 1, 0)",
                          (self.id,))
           conn.commit()
       finally:
           conn.close()


   def delete_product(self, mydb):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       try:
           cursor.execute("DELETE FROM product_store_stock WHERE product = %s",(self.id,))
           cursor.execute("DELETE FROM product_storage_stock WHERE product = %s", (self.id,))
           cursor.execute("DELETE FROM product WHERE id = %s", (self.id,))
           conn.commit()
       finally:
           conn.close()


   def show_notes(self, mydb, store):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT note_text FROM product_note WHERE product = %s AND store = %s", (self.id, store))
       rows = cursor.fetchall()
       notes = []
       for row in rows:
           notes.append(row[0])
       conn.close()
       return notes


   def insert_notes(self, mydb, store, note):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       try:
           cursor.execute("INSERT INTO product_note VALUES (%s, %s,%s)",(self.id, store, note))
           conn.commit()
       finally:
           conn.close()




class StoreOrder:
   def __init__(self, order_id, store, priority, status, start_date, end_date, products, amounts):
       self.id = order_id
       self.store = store
       self.priority = priority
       self.status = status
       self.start_date = start_date
       self.end_date = end_date
       self.products = products
       self.amounts = amounts


   def insert_order(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("INSERT INTO store_order(store, storage, priority, status, start_date) VALUES "
                          "(%s, %s, %s, %s, CURRENT_DATE())", (self.store, 1, self.priority, 'PENDING'))
           cursor.execute("SELECT MAX(id) FROM store_order")
           result = cursor.fetchone()
           self.id = result[0]
           for p, a in zip(self.products, self.amounts):
               cursor.execute("INSERT INTO store_order_product VALUES (%s, %s, %s)", (self.id, p, a))
           conn.commit()
       finally:
           conn.close()


   def complete_order(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("UPDATE store_order SET status = %s, end_date = CURRENT_DATE() WHERE id = %s",
                          ("COMPLETED", self.id))
           for p, a in zip(self.products, self.amounts):
               cursor.execute("SELECT stock FROM product_store_stock WHERE product = %s AND store = %s",
                              (p, self.store))
               result = cursor.fetchone()
               stock = result[0] + a
               cursor.execute("UPDATE product_store_stock SET stock = %s WHERE product = %s AND store = %s",
                              (stock, p, self.store))
           conn.commit()
       finally:
           conn.close()


   def cancel_order(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("UPDATE store_order SET status = %s, end_date = CURRENT_DATE() WHERE id = %s",
                          ("CANCELED", self.id))
           conn.commit()
       finally:
           conn.close()


   def confirm_order(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("UPDATE store_order SET status = %s, end_date = CURRENT_DATE() WHERE id = %s",
                          ("CONFIRMED", self.id))
           conn.commit()


       finally:
           conn.close()


   def send_order(self,mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("UPDATE store_order SET status = %s, end_date = CURRENT_DATE() WHERE id = %s",
                          ("SENT", self.id))
           for p, a in zip(self.products, self.amounts):
               cursor.execute("SELECT stock FROM product_store_stock WHERE product = %s AND store = %s",
                              (p, self.store))
               result = cursor.fetchone()
               stock = result[0] - a
               cursor.execute("UPDATE product_store_stock SET stock = %s WHERE product = %s AND store = %s",
                              (stock, p, self.store))
           conn.commit()
       finally:
           conn.close()


class StorageOrder:
   def __init__(self, order_id, status, start_date, end_date, products, amounts):
       self.id = order_id
       self.status = status
       self.start_date = start_date
       self.end_date = end_date
       self.products = products
       self.amounts = amounts


   def insert_order(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("INSERT INTO storage_order(storage, status, start_date) VALUES "
                          "(%s, %s, CURRENT_DATE())", (1, 'PENDING'))
           cursor.execute("SELECT MAX(id) FROM storage_order")
           result = cursor.fetchone()
           self.id = result[0]
           for p, a in zip(self.products, self.amounts):
               cursor.execute("INSERT INTO storage_order_product VALUES (%s, %s, %s)",
                              (self.id, p, a))
           conn.commit()
       finally:
           conn.close()


   def complete_order(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("UPDATE storage_order SET status = %s, end_date = CURRENT_DATE() WHERE id = %s",
                          ("COMPLETED", self.id))
           for p, a in zip(self.products, self.amounts):
               cursor.execute("SELECT stock FROM product_storage_stock WHERE product = %s AND storage = %s",
                              (p, self.id))
               result = cursor.fetchone()
               result = result + a
               cursor.execute("UPDATE product_storage_stock SET stock = %s WHERE product = %s AND storage = %s",
                              (result, p, self.id))
           conn.commit()
       finally:
           conn.close()


   def cancel_order(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("UPDATE storage_order SET status = %s, end_date = CURRENT_DATE() WHERE id = %s",
                          ("CANCELED", self.id))
           conn.commit()
       finally:
           conn.close()




class StoreSale:
   def __init__(self, sale_id, store, date, products, amounts):
       self.id = sale_id
       self.store = store
       self.date = date
       self.products = products
       self.amounts = amounts


   def insert_sale(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("INSERT INTO store_sale(store, sale_date) VALUES "
                          "(%s, CURRENT_DATE())", (self.store,))
           cursor.execute("SELECT MAX(id) FROM store_sale")
           result = cursor.fetchone()
           self.id = result[0]
           for p, a in zip(self.products, self.amounts):
               cursor.execute("INSERT INTO store_sale_product VALUES (%s, %s, %s)", (self.id, p, a))
               cursor.execute("SELECT stock FROM product_store_stock WHERE product = %s AND store = %s",
                              (p, self.store))
               result = cursor.fetchone()
               stock = result[0] - a
               cursor.execute("UPDATE product_store_stock SET stock = %s WHERE product = %s AND store = %s",
                              (stock, p, self.store))
           conn.commit()
       finally:
           conn.close()




class WorkerShift:
   def __init__(self, worker, date, start_time, end_time):
       self.worker = worker
       self.date = date
       self.start_time = start_time
       self.end_time = end_time


   def insert_store_shift(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("INSERT INTO store_worker_shift VALUES (%s, %s, %s, %s)",
                          (self.worker, self.date, self.start_time, self.end_time))
           conn.commit()
       finally:
           conn.close()


   def insert_storage_shift(self, mydb):
       conn = mydb.connect_db()
       try:
           cursor = conn.cursor()
           cursor.execute("INSERT INTO storage_worker_shift VALUES (%s, %s, %s, %s)",
                          (self.worker, self.date, self.start_time, self.end_time))
           conn.commit()
       finally:
           conn.close()

