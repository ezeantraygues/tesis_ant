# Create chain that takes .jpg file as input and extracts data from it. Finally put the data to the database
import os
from dotenv import load_dotenv
load_dotenv('.env.dev')

from src.common.mongo_manager import MongoManager
from src.common.gdrive_manager import Uploader
from src.data_extractor.upload_vectors import upload_vectors
from src.data_extractor.extract_data import extract_data_from_image
from src.preprocessing.preprocess_files import DataPreprocessor

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
GDRIVE_PLOTS_FOLDER_ID = os.getenv('GDRIVE_PLOTS_FOLDER_ID')

mongo_manager = MongoManager(MONGO_URI, MONGO_DATABASE)

def process_file(pdf_path: str):

    with open(pdf_path, 'rb') as file:
        pdf_content = file.read()
        pdf_image = DataPreprocessor(pdf_content)()

    extracted_data = extract_data_from_image(pdf_image)

    # Save to Mongo
    full_data = {**extracted_data['patient_data'], **extracted_data['quantitative_data'], **extracted_data['text_fields']}
    mongo_manager.put_item(MONGO_COLLECTION, full_data)
    
    # Save to GDrive
    for plot_path in extracted_data['plots'][1]:
        Uploader().upload_file(plot_path,parent_folder_id=GDRIVE_PLOTS_FOLDER_ID)

    # #Upload 'Resultados" & 'Conclusiones' to vector store (pinecone)
    upload_vectors(extracted_data['text_fields'], extracted_data['patient_data'])


    return extracted_data
