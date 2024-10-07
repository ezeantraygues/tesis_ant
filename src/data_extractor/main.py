# Create chain that takes .jpg file as input and extracts data from it. Finally put the data to the database
from common.database_manager import DatabaseManager
from common.gdrive_manager import GdriveManager
from data_extractor import upload_vectors
from data_extractor.extract_data import extract_data_from_image
from preprocessing.preprocess_files import DataPreprocessor

dataprocessor = DataPreprocessor()
database_manager = DatabaseManager()
gdrive_manager = GdriveManager()


def process_file(pdf_url: str):
    pdf_image = dataprocessor.convert_pdf_to_img(pdf_url)

    extracted_data = extract_data_from_image(pdf_image)

    #TODO: separate each item in the corresponding db
    database_manager.put_item(extracted_data['data'])
    
    gdrive_manager.put_item(extracted_data['plots'])

    #Upload 'Resultados" & 'Conclusiones' to vector store (pinecone)
    upload_vectors()
