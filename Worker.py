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
