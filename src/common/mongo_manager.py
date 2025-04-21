# src/common/mongo_manager.py

from pymongo import MongoClient
from typing import Dict, Any, List
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv('.env.dev')

class MongoManager:
    def __init__(self, uri: str, db_name: str):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            print(f"Conexión a MongoDB Atlas exitosa: Base de datos '{db_name}'.")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")
            raise

    def put_item(self, collection_name: str, item: Dict[str, Any]) -> ObjectId:
        """Inserta un nuevo documento en la colección y devuelve el ID insertado."""
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(item)
            return result.inserted_id
        except Exception as e:
            print(f"Error al insertar documento: {e}")
            return None

    def get_item(self, collection_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Recupera un documento de la colección basado en la consulta."""
        try:
            collection = self.db[collection_name]
            return collection.find_one(query)
        except Exception as e:
            print(f"Error al recuperar documento: {e}")
            return None

    def update_item(self, collection_name: str, query: Dict[str, Any], new_values: Dict[str, Any]) -> int:
        """Actualiza un documento en la colección basado en la consulta."""
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {"$set": new_values})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar documento: {e}")
            return 0

    def update_document_by_id(self, collection_name: str, document_id: str, update_fields: Dict[str, Any]) -> bool:
        """Actualiza un documento en la colección por su ObjectId."""
        try:
            collection = self.db[collection_name]
            result = collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al actualizar documento por ID: {e}")
            return False

    def delete_item(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Elimina un documento de la colección basado en la consulta."""
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error al eliminar documento: {e}")
            return 0

    def get_collection_data(self, collection_name: str, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los documentos de una colección opcionalmente filtrando por una consulta."""
        try:
            collection = self.db[collection_name]
            if query is None:
                query = {}
            return list(collection.find(query))
        except Exception as e:
            print(f"Error al recuperar datos de la colección: {e}")
            return []

