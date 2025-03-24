from pymongo import MongoClient
from typing import Dict, Any
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv('.env.dev')

class MongoManager:
    def __init__(self, uri, db_name):
        """Inicializa la conexión a MongoDB Atlas."""
        try:
            # uri = os.getenv("MONGO_URI")
            # db_name = os.getenv("MONGO_DB_NAME", "prueba_informes")  # Nombre por defecto
            # if not uri:
            #     raise ValueError("MONGO_URI no está definida en el archivo .env.")
            
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            print(f"Conexión a MongoDB Atlas exitosa: Base de datos '{db_name}'.")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")
            raise

    def put_item(self, collection_name: str, item: Dict[str, Any]):
        """Inserta un nuevo documento en la colección."""
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(item)
            return result.inserted_id
        except Exception as e:
            print(f"Error al insertar documento: {e}")
            return None

    def get_item(self, collection_name: str, query: Dict[str, Any]):
        """Recupera un documento de la colección basado en la consulta."""
        try:
            collection = self.db[collection_name]
            return collection.find_one(query)
        except Exception as e:
            print(f"Error al recuperar documento: {e}")
            return None

    def update_item(self, collection_name: str, query: Dict[str, Any], new_values: Dict[str, Any]):
        """
        Actualiza un documento en la colección basado en la consulta.
        :return: El número de documentos modificados (1 si se modificó, 0 si no se encontró).
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, new_values)
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar documento: {e}")
            return 0

    def delete_item(self, collection_name: str, query: Dict[str, Any]):
        """
        Elimina un documento de la colección basado en la consulta.
        :return: El número de documentos eliminados.
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error al eliminar documento: {e}")
            return 0
        
    def get_collection_data(self, collection_name, query=None):
   # """Retrieve documents from a collection with an optional query."""
        try:
            collection = self.db[collection_name]
            if query is None:
              query = {}
            return list(collection.find(query))
        except Exception as e:
            print(f"Error al recuperar datos de la colección: {e}")
            return []