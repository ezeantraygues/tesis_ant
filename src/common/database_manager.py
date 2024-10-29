from pymongo import MongoClient
from typing import Dict, Any

class DatabaseManager:
    def __init__(self, uri: str, db_name: str):
        """Inicializa la conexión a MongoDB Atlas."""
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def put_item(self, collection_name: str, item: Dict[str, Any]):
        """Inserta un nuevo documento en la colección."""
        collection = self.db[collection_name]
        result = collection.insert_one(item)
        return result.inserted_id

    def get_item(self, collection_name: str, query: Dict[str, Any]):
        """Recupera un documento de la colección basado en la consulta."""
        collection = self.db[collection_name]
        return collection.find_one(query)

    def update_item(self, collection_name: str, query: Dict[str, Any], new_values: Dict[str, Any]):
        """
        Actualiza un documento en la colección basado en la consulta.

        :param collection_name: El nombre de la colección donde se va a actualizar el documento.
        :param query: La consulta utilizada para encontrar el documento que se va a actualizar.
        :param new_values: Un diccionario con los nuevos valores a actualizar.
        :return: El número de documentos modificados (1 si se modificó, 0 si no se encontró).
        """
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": new_values})
        return result.modified_count

    def delete_item(self, collection_name: str, query: Dict[str, Any]):
        """
        Elimina un documento de la colección basado en la consulta.

        :param collection_name: El nombre de la colección de la que se eliminará el documento.
        :param query: La consulta utilizada para encontrar el documento que se va a eliminar.
        :return: El número de documentos eliminados.
        """
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count



# from pymongo import MongoClient
# from typing import Dict, Any

# class DatabaseManager:
#     def __init__(self, uri: str, db_name: str):
#         """Inicializa la conexión a MongoDB Atlas."""
#         self.client = MongoClient(uri)
#         self.db = self.client[db_name]

#     def put_item(self, collection_name: str, item: Dict[str, Any]):
#         collection = self.db[collection_name]
#         result = collection.insert_one(item)
#         return result.inserted_id

#     def get_item(self, collection_name: str, query: Dict[str, Any]):
#         collection = self.db[collection_name]
#         return collection.find_one(query)
    
#     def update_item(self, collection_name: str, query: Dict[str, Any], new_values: Dict[str, Any]):
#     # """
#     # Actualiza un documento en la colección basado en la consulta.

#     # :param collection_name: El nombre de la colección donde se va a actualizar el documento.
#     # :param query: La consulta utilizada para encontrar el documento que se va a actualizar.
#     # :param new_values: Un diccionario con los nuevos valores a actualizar.
#     # :return: El número de documentos modificados (1 si se modificó, 0 si no se encontró).
#     # """
#      collection = self.db[collection_name]  # Accede a la colección
#      result = collection.update_one(query, {"$set": new_values})  # Actualiza el documento con los nuevos valores
#      return result.modified_count  # Devuelve la cantidad de documentos modificados (generalmente 1 o 0)

# #TODO: crear conector para mongodb

# if __name__ == "__main__":
#     URI = "mongodb+srv://ezeantraygues:46w1pB9TBeWOncgV@cluster0.i6kji.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# uri = "mongodb+srv://ezeantraygues:46w1pB9TBeWOncgV@cluster0.i6kji.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
#     DB_NAME = "test_db"
    
#     db_manager = DatabaseManager(URI, DB_NAME)
#     print("Instancia creada exitosamente.")




