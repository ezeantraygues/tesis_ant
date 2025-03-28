SYSTEM_CONTENT = """
You'll receive a free text written by an user, who wants to query a mongo database.
The database has a collection with documents, each of them with the following attributes:
{{
    paciente: str
    patologia: str
    session_notes: str
    fecha_nacimiento: str
    peso: str
    altura: str
    sexo: str
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
}}

You must return a query in mongo query language that can then be applied to the database, in the format
{{"query":"your mongo query"}}

"""

USER_MESSAGE = """
Here's the user free text:
{text}
"""