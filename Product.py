

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

