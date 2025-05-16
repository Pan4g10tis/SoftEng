class StorageManager:
   def __init__(self, username, password, name, surname, email, phone, storage):
       self.username = username
       self.password = password
       self.name = name
       self.surname = surname
       self.email = email
       self.phone = phone
       self.storage = storage

   def get_storage(self, mydb):
       conn = mysql.connector.connect(
           host=mydb.host,
           user=mydb.user,
           password=mydb.password,
           database=mydb.database)
       cursor = conn.cursor()
       cursor.execute("SELECT id, address, email, phone FROM store INNER JOIN store_manager WHERE username = %s",
           (self.username,))
       result = cursor.fetchone()
       conn.close()
       my_storage = Storage(*result)
       return my_storage

   @classmethod
   def create(cls, mydb, username):
       conn = mydb.connect_db()
       cursor = conn.cursor()
       cursor.execute("SELECT manager.username, password, name, surname, email, phone, storage "
                      "FROM manager INNER JOIN storage_manager On manager.username = storage_manager.username "
                      "WHERE manager.username = %s", (username,))
       result = cursor.fetchone()
       manager = StorageManager(*result)
       return manager
