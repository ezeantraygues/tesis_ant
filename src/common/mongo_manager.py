from pymongo import MongoClient
from typing import Dict, Any



class MongoManager:
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