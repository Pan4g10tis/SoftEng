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
