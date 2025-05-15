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

