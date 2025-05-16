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
