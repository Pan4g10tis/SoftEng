class StoreManager:
   def __init__(self, username, password, name, surname, email, phone, store):
       self.username = username
       self.password = password
       self.name = name
       self.surname = surname
       self.email = email
       self.phone = phone
       self.store = store


   def get_store(self, mydb):
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
       my_store = Store(*result)
       return my_store

