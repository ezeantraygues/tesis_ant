# Create pydantic model with report data
from pydantic import BaseModel


class DataExtractorResponse(BaseModel):
    #TODO: completar con todos los parámetros
    cadencia:str