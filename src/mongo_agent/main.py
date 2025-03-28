
import json
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from models.mongo_query import Text2Mongo
from src.common.mongo_manager import MongoManager
from .prompts import SYSTEM_CONTENT, USER_MESSAGE

chat = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    request_timeout=550,
    max_tokens=4000,
)

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
mongo_manager = MongoManager(MONGO_URI, MONGO_DATABASE)

def query_mongodb(text:str):
    system_message = SystemMessage(content=SYSTEM_CONTENT)
    user_message = HumanMessage(content=USER_MESSAGE.format(text=text))

    history = [system_message, user_message]
    response = chat.invoke(history, response_format=Text2Mongo)
    query = json.loads(json.loads(response.content)['query'])
    print(f"Query generada: {query}")
    items = mongo_manager.get_item(collection_name=MONGO_COLLECTION,query = query)
    print(f"Items encontrados: {items}")
    return items


