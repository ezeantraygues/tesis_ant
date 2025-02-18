import streamlit as st
import pandas as pd
import os
import sys
import pymongo
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(".env.dev")

# Añadir ruta al sys.path para imports personalizados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.preprocessing.preprocess_files import DataPreprocessor
from src.data_extractor.extract_data import extract_data_from_image

# Configuración de MongoDB
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = "informes"

# Conectar a MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]

# Configuración de Streamlit
st.set_page_config(page_title="Procesamiento", layout="wide")

def main():
    st.title("Procesamiento de Informes")

    # Selección entre nuevo informe o búsqueda
    option = st.radio("Seleccione una opción:", ("Subir nuevo informe", "Buscar informe existente"))

    if option == "Subir nuevo informe":
        uploaded_file = st.file_uploader("Subir archivo PDF", type=["pdf"])
        
        if uploaded_file is not None:
            st.success("Archivo subido correctamente")

            # Leer archivo PDF
            pdf_content = uploaded_file.read()

            # Convertir PDF a imágenes en Base64 usando DataPreprocessor
            try:
                data_preprocessor = DataPreprocessor(pdf_content)
                encoded_images = data_preprocessor()
                st.write(f"Imágenes procesadas y codificadas: {len(encoded_images)}")
            except Exception as e:
                st.error(f"Error al convertir PDF a imágenes: {e}")
                encoded_images = []

            # Extraer datos con Azure OpenAI
            extracted_data = {}
            if encoded_images:
                try:
                    extracted_data = extract_data_from_image(encoded_images)
                    st.success("Datos extraídos correctamente")
                except Exception as e:
                    st.error(f"Error al extraer datos: {e}")

            # Mostrar datos extraídos
            st.markdown("### Datos Extraídos")
            st.json(extracted_data)

            # Campos de texto editables
            resultados = st.text_area("Resultados", extracted_data.get("resultados", ""))
            conclusiones = st.text_area("Conclusiones", "")
            recomendaciones = st.text_area("Recomendaciones", "")

            # Botón para guardar en MongoDB
            if st.button("Guardar en BD"):
                patient_data = {
                    "nombre": extracted_data.get("nombre", "Desconocido"),
                    "quantitative_data": extracted_data.get("quantitative_data", {}),
                    "imagenes": encoded_images,
                    "resultados": resultados,
                    "conclusiones": conclusiones,
                    "recomendaciones": recomendaciones
                }
                try:
                    inserted_id = collection.insert_one(patient_data).inserted_id
                    st.success(f"Datos guardados correctamente en MongoDB con ID: {inserted_id}")
                except Exception as e:
                    st.error(f"Error guardando datos en MongoDB: {e}")

    elif option == "Buscar informe existente":
        paciente = st.text_input("Ingrese el nombre del paciente")
        if st.button("Buscar"):
            informe = collection.find_one({"nombre": paciente})
            if informe:
                st.markdown("### Datos del Informe")
                st.write(pd.DataFrame(informe["quantitative_data"], index=[0]))

                # Permitir edición de conclusiones y recomendaciones
                nuevas_conclusiones = st.text_area("Conclusiones", informe.get("conclusiones", ""))
                nuevas_recomendaciones = st.text_area("Recomendaciones", informe.get("recomendaciones", ""))

                if st.button("Actualizar Conclusiones"):
                    collection.update_one({"nombre": paciente}, {"$set": {"conclusiones": nuevas_conclusiones}})
                    st.success("Conclusiones actualizadas")

                if st.button("Actualizar Recomendaciones"):
                    collection.update_one({"nombre": paciente}, {"$set": {"recomendaciones": nuevas_recomendaciones}})
                    st.success("Recomendaciones actualizadas")
            else:
                st.error("No se encontró el informe del paciente")

if __name__ == "__main__":
    main()

#--------------------------------------------------------------------------------------------------------------------
# import streamlit as st
# import pandas as pd
# import os
# import sys
# import pymongo
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from src.preprocessing.preprocess_files import DataPreprocessor
# from src.data_extractor.extract_data import extract_text_data, extract_plots_from_image


# # Cargar variables de entorno
# from dotenv import load_dotenv
# load_dotenv(".env.dev")


# # Cargar el archivo .env.dev
# #load_dotenv(dotenv_path=r"C:\Users\ezean\OneDrive\Escritorio\tesis_ant\.env.dev")

# # Verificar todas las variables de entorno cargadas
# print(os.environ)

# # Ruta absoluta al archivo .env.dev
# #dotenv_path = os.path.abspath(r"C:\Users\ezean\OneDrive\Escritorio\tesis_ant\.env.dev")

# # Cargar el archivo .env.dev
# #load_dotenv(dotenv_path=dotenv_path)

# # Cargar variables de entorno
# #load_dotenv(dotenv_path=r"C:\\Users\\ezean\\OneDrive\\Escritorio\\tesis_ant\\.env.dev")
# MONGO_URI = os.getenv('MONGO_URI')
# MONGO_DATABASE = os.getenv('MONGO_DATABASE')
# MONGO_COLLECTION = "informes"






# # Conectar a MongoDB
# client = pymongo.MongoClient(MONGO_URI)
# db = client[MONGO_DATABASE]
# collection = db[MONGO_COLLECTION]

# # Streamlit config
# st.set_page_config(page_title="Procesamiento", layout="wide")

# def main():
#     st.title("Procesamiento de Informes")
    
#     # Selección entre nuevo informe o búsqueda
#     option = st.radio("Seleccione una opción:", ("Subir nuevo informe", "Buscar informe existente"))
    
#     if option == "Subir nuevo informe":
#         uploaded_file = st.file_uploader("Subir archivo PDF", type=["pdf"])
#         if uploaded_file is not None:
#             st.success("Archivo subido correctamente")
            
#             # Leer archivo PDF
#             pdf_content = uploaded_file.read()
            
#             # Extraer datos e imágenes con manejo de errores
#             try:
#                 text_data = extract_text_data(pdf_content) if pdf_content else {}
#                 images = extract_plots_from_image(pdf_content) if pdf_content else []
#             except Exception as e:
#                 st.error(f"Error al procesar el archivo: {e}")
#                 text_data, images = {}, []
            
#             # Mostrar datos extraídos
#             st.markdown("### Datos Extraídos")
#             st.write(pd.DataFrame(text_data, index=[0]))
            
#             # Campos de texto editables
#             resultados = st.text_area("Resultados", text_data.get("resultados", ""))
#             conclusiones = st.text_area("Conclusiones", "")
#             recomendaciones = st.text_area("Recomendaciones", "")
            
#             # Botón para guardar en MongoDB
#             if st.button("Guardar en BD"):
#                 patient_data = {
#                     "nombre": text_data.get("nombre", "Desconocido"),
#                     "quantitative_data": text_data.get("quantitative_data", {}),
#                     "imagenes": images,
#                     "resultados": resultados,
#                     "conclusiones": conclusiones,
#                     "recomendaciones": recomendaciones
#                 }
#                 try:
#                     inserted_id = collection.insert_one(patient_data).inserted_id
#                     st.success(f"Datos guardados correctamente en MongoDB con ID: {inserted_id}")
#                 except Exception as e:
#                     st.error(f"Error guardando datos en MongoDB: {e}")
    
#     elif option == "Buscar informe existente":
#         paciente = st.text_input("Ingrese el nombre del paciente")
#         if st.button("Buscar"):
#             informe = collection.find_one({"nombre": paciente})
#             if informe:
#                 st.markdown("### Datos del Informe")
#                 st.write(pd.DataFrame(informe["quantitative_data"], index=[0]))
                
#                 # Permitir edición de conclusiones y recomendaciones
#                 nuevas_conclusiones = st.text_area("Conclusiones", informe.get("conclusiones", ""))
#                 nuevas_recomendaciones = st.text_area("Recomendaciones", informe.get("recomendaciones", ""))
                
#                 if st.button("Actualizar Conclusiones"):
#                     collection.update_one({"nombre": paciente}, {"$set": {"conclusiones": nuevas_conclusiones}})
#                     st.success("Conclusiones actualizadas")
                
#                 if st.button("Actualizar Recomendaciones"):
#                     collection.update_one({"nombre": paciente}, {"$set": {"recomendaciones": nuevas_recomendaciones}})
#                     st.success("Recomendaciones actualizadas")
#             else:
#                 st.error("No se encontró el informe del paciente")

# if __name__ == "__main__":
#     main()
#----------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import pandas as pd
# import os

# # Streamlit app configuration
# st.set_page_config(page_title="Procesamiento", layout="wide")

# def image_carousel(image_list):
#     """Displays an image carousel given a list of image URLs or paths."""
#     if len(image_list) > 0:
#         selected_image = st.slider(
#             "Carousel", 0, len(image_list) - 1, 0, format="Image %d"
#         )
#         st.image(image_list[selected_image], use_column_width=True, caption=f"Image {selected_image + 1}")
#     else:
#         st.write("No images available to display.")

# def main():
#     st.title("Procesamiento")

#     # Layout for inputs, results, and buttons
#     col1, col2 = st.columns([1, 3])

#     with col1:
#         # File upload box
#         uploaded_file = st.file_uploader("Subir archivo.pdf", type=["pdf"])
#         if uploaded_file is not None:
#             st.write("File uploaded successfully!")

#         # Write results section (placeholder for future implementation)
#         st.text_area("Resultados", "Resultados del paciente")
#         st.text_area("Conclusiones", "Conclusiones del paciente")
#         st.text_area("Recomendaciones", "Recomendaciones del paciente")

#     with col2:
#         # Centered "Datos extraídos" header
#         st.markdown("<h3 style='text-align: center;'>Datos extraídos</h3>", unsafe_allow_html=True)

#         # DataFrame visualization
#         # Example DataFrame
#         data = pd.read_csv('example_data/jhon_doe.csv')
#         df = pd.DataFrame(data)
#         st.dataframe(df, use_container_width=True)

#         # Horizontal buttons below the table
#         st.markdown("<hr>", unsafe_allow_html=True)
#         col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)

#         with col_btn1:
#             if st.button("Edit"):
#                 st.write("Edit functionality triggered!")  # Placeholder for edit logic

#         with col_btn3:
#             if st.button("Save"):
#                 st.write("Save functionality triggered!")  # Placeholder for save logic
        
#         with col_btn2:
#             if st.button("Cancel"):
#                 st.write("Cancel functionality triggered!")  # Placeholder for cancel logic

#         with col_btn4:
#             if st.button("Save & Gen. report"):
#                 st.write("Save and generate report functionality triggered!")  # Placeholder for report logic

#         with col_btn5:
#             if st.button("Print"):
#                 st.write("Print functionality triggered!")  # Placeholder for print logic

#         # Image carousel
#         st.subheader("Graficos")
#         # Example image list (replace with your images)
#         image_list = [f'example_data/plots/{plot}' for plot in os.listdir('example_data/plots')]
#         image_carousel(image_list)

# if __name__ == "__main__":
#     main()
