from pydantic import BaseModel

class Text2Mongo(BaseModel):
    query: str