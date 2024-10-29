from database_manager import DatabaseManager

# Configura la URI y el nombre de la base de datos
URI = "mongodb+srv://ezeantraygues:46w1pB9TBeWOncgV@cluster0.i6kji.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "your_database_name"

# Inicializa el DatabaseManager
db_manager = DatabaseManager(URI, DB_NAME)

# Prueba de inserción de un item
item = {"name": "Test Item", "value": 42}
inserted_id = db_manager.put_item("your_collection_name", item)
print(f"Inserted item with ID: {inserted_id}")

# Prueba de obtención de un item
query = {"_id": inserted_id}
retrieved_item = db_manager.get_item("your_collection_name", query)
print(f"Retrieved item: {retrieved_item}")


# Actualiza el item
new_values = {"value": 100}
updated_count = db_manager.update_item("your_collection_name", {"_id": inserted_id}, new_values)
print(f"Updated {updated_count} item(s).")

# Verifica la actualización
retrieved_item_after_update = db_manager.get_item("your_collection_name", {"_id": inserted_id})
print(f"Retrieved item after update: {retrieved_item_after_update}")

# Elimina el item
deleted_count = db_manager.delete_item("your_collection_name", {"_id": inserted_id})
print(f"Deleted {deleted_count} item(s).")
