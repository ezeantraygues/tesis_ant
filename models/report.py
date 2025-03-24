# Create pydantic model with report data
from pydantic import BaseModel
from typing import Optional

class PatientData(BaseModel):
    paciente: str
    patologia: str
    session_notes: str
    fecha_nacimiento: str
    peso: str
    altura: str
    sexo: str

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
    patient_data:PatientData
    quantitative_data:QuantitativeData
    text_fields:TextFields  