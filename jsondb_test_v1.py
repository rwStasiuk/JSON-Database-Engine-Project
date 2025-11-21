from jsondb_v1 import JSONDB

db = JSONDB("data_v1.json")
db.load()
db.addC("users")
db.addI("users", "Alice")
db.setValue("users", "Alice", "email", "alice@example.com")
db.save()
