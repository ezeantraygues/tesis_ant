from src.common.pinecone_manager import PineconeManager


def upload_vectors(text_fields:dict, patient_data:dict):
    """ 
        text_fields: dict with keys ("Resultados","Conclusiones","Recomendaciones") 
    """
    pinecone = PineconeManager()
    
    vector_list = []
    for k,v in text_fields.items():
        vector_list.append(tuple(v, vector_metadata = {"type":k,**patient_data}))

    #save vector to pinecone
    pinecone.upload(vector_list)