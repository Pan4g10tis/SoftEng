

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

