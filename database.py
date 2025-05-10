class DataBase:
   def __init__(self, user, password, host, database):
       self.user = user
       self.password = password
       self.host = host
       self.database = database

   def connect_db(self):
       return mysql.connector.connect(
           user=self.user,
           password=self.password,
           host=self.host,
           database=self.database
       )


