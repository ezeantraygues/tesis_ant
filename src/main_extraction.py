# Create chain that takes .jpg file as input and extracts data from it. Finally put the data to the database
import os
from dotenv import load_dotenv
load_dotenv('.env.dev')

from src.common.mongo_manager import MongoManager
from src.common.gdrive_manager import Uploader
# from data_extractor import upload_vectors
from src.data_extractor.extract_data import extract_data_from_image
from src.preprocessing.preprocess_files import DataPreprocessor

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')


mongo_manager = MongoManager(MONGO_URI,MONGO_DATABASE)

def process_file(pdf_path: str):

    with open(pdf_path, 'rb') as file:
        pdf_content = file.read()
        pdf_image = DataPreprocessor(pdf_content)()

    extracted_data = extract_data_from_image(pdf_image)

    #TODO: separate each item in the corresponding db
    mongo_manager.put_item(MONGO_COLLECTION, extracted_data['quantitative_data'])


    
    file_id = Uploader().upload_file(pdf_path,'1TqqPUARbUFWpOnGEkufm2xkrHuUF_vIH')#extracted_data['plots'])

    # #Upload 'Resultados" & 'Conclusiones' to vector store (pinecone)
    # upload_vectors(extracted_data['text_fields'])
