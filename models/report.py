# Create pydantic model with report data
from pydantic import BaseModel
from typing import Optional

class DataExtractorResponse(BaseModel):
    #TODO: completar con todos los parámetros
    cadencia:Optional[str]
    tipo_contacto: Optional[str]
    inclinacion_tronco: Optional[str]
    progresion: Optional[str]
    indice_simetria: Optional[str]
    velocidad_propulsion: Optional[str]
    capacidad_amortiguacion: Optional[str]
    rango_anteversion: Optional[str]
    rango_rotacion_pelvica: Optional[str]
    FRP: Optional[str]
    activacion_muscular_apoyo: Optional[str]
    activacion_muscular_oscilacion: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "cadencia": "90 pasos/minuto",
                "tipo_contacto": "talón",
                "inclinacion_tronco": "normal",
                "progresion": "rectilínea",
                "indice_simetria": "95%",
                "velocidad_propulsion": "1.5 m/s",
                "capacidad_amortiguacion": "buena",
                "rango_anteversion": "15°",
                "rango_rotacion_pelvica": "8°",
                "FRP": "normal",
                "activacion_muscular_apoyo": "sobreactivación",
                "activacion_muscular_oscilacion": "normal"
            }
        }