class StoreManager:
   def __init__(self, username, password, name, surname, email, phone, store):
       self.username = username
       self.password = password
       self.name = name
       self.surname = surname
       self.email = email
       self.phone = phone
       self.store = store


   @classmethod
   def get_storage(cls, store_id, address, email, phone):
       my_store = Store(store_id, address, email, phone)
