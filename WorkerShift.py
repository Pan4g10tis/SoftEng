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


