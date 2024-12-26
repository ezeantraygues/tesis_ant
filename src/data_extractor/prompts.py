SYSTEM_CONTENT = """
You'll receive images from a biomechanical report of a patient, showing data in different formats. Your task is to extract the following data and return it as a json:

{{
    patient_data: {{
            PACIENTE: str
            
        }},
    quantitative_data: {{
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
        }},
    text_fields: {{
        resultados:str
        conclusiones:str
        recomendaciones:str
    }}
}}

"""
USER_TEXT_CONTENT = """
Consider the given images of the form to extract the requested data.
"""
