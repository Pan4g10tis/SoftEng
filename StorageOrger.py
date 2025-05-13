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
