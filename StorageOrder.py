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
                cursor.execute("INSERT INTO storage_order_product VALUES %s, %s, %s",
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

