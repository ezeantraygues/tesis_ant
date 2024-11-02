# Create pydantic model with report data
from pydantic import BaseModel
from typing import Optional

class QuantitativeData(BaseModel):
    #TODO: completar con todos los parámetros
    cadencia: str
    tipo_contacto: str
    inclinacion_tronco: str
    progresion: str
    indice_simetria: str
    velocidad_propulsion: str
    capacidad_amortiguacion: str
    rango_anteversion: str
    rango_rotacion_pelvica: str
    FRP: str
    activacion_muscular_apoyo: str
    activacion_muscular_oscilacion: str

class TextFields(BaseModel):
    resultados:str
    conclusiones:str
    recomendaciones:str
    

class DataExtractorResponse(BaseModel):
    quantitative_data:QuantitativeData
    text_fields:TextFields  

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "cadencia": "90 pasos/minuto",
    #             "tipo_contacto": "talón",
    #             "inclinacion_tronco": "normal",
    #             "progresion": "rectilínea",
    #             "indice_simetria": "95%",
    #             "velocidad_propulsion": "1.5 m/s",
    #             "capacidad_amortiguacion": "buena",
    #             "rango_anteversion": "15°",
    #             "rango_rotacion_pelvica": "8°",
    #             "FRP": "normal",
    #             "activacion_muscular_apoyo": "sobreactivación",
    #             "activacion_muscular_oscilacion": "normal"
    #         }
    #     }