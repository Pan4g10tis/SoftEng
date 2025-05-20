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
