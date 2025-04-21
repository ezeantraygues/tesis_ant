
# # En este funciona Guardar cambios y Descargar pdf pero alguna que otra vez me hace problemas con el toma de los tokens 
# "Openai.LengthFinishReasonError: Could not parse response content as the length limit was reached"
import os
import sys
import tempfile
import streamlit as st
import pandas as pd

# Agrega el directorio principal al path del sistema para importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importa funciones y clases necesarias
from src.main_extraction import process_file
from src.generate_sections.main import write_report_from_data
from src.common.mongo_manager import MongoManager
#esto es para el boton descargar
from fpdf import FPDF
from PyPDF2 import PdfMerger
from src.common.gdrive_manager import Uploader

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

# Configura la página en Streamlit
st.set_page_config(page_title="Procesamiento", layout="wide")

# Inicializa la conexión con la base de datos
mongo_manager = MongoManager(MONGO_URI, MONGO_DATABASE)

@st.cache_data
def process_pdf(file_path):
    return process_file(file_path)

def generate_text(data, results, text_type):
    return write_report_from_data(data, results, text_type)

def image_carousel(image_list):
    if image_list:
        selected_image = st.slider("Carousel", 0, len(image_list) - 1, 0, format="Imagen %d")
        st.image(image_list[selected_image], use_column_width=True, caption=f"Imagen {selected_image + 1}")
    else:
        st.write("No hay imágenes para mostrar.")

def display_tables(extracted_data):
    st.markdown("<h3 style='text-align: center;'>Datos personales del paciente</h3>", unsafe_allow_html=True)
    df_patient = pd.DataFrame({k: [v] for k, v in extracted_data['patient_data'].items()})
    edited_patient = st.data_editor(df_patient, use_container_width=True, key="df_patient")

    st.markdown("<h3 style='text-align: center;'>Datos cuantitativos del paciente</h3>", unsafe_allow_html=True)
    df_quant = pd.DataFrame({k: [v] for k, v in extracted_data['quantitative_data'].items()})
    edited_quant = st.data_editor(df_quant, use_container_width=True, key="df_quant")

    # Actualizamos los datos en session_state
    extracted_data['patient_data'] = edited_patient.to_dict(orient='records')[0]
    extracted_data['quantitative_data'] = edited_quant.to_dict(orient='records')[0]

#esto es para el botn descargar
def create_text_fields_pdf(text_fields, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, title in [("resultados", "Resultados"), ("conclusiones", "Conclusiones"), ("recomendaciones", "Recomendaciones")]:
        content = text_fields.get(key, "")
        pdf.set_font("Arial", "B", 11)#14
        pdf.cell(0, 5, title, ln=True)#pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", "", 10)#12
        for line in content.split("\n"):
            pdf.multi_cell(0, 5, line)#pdf.multi_cell(0, 10, line)
        pdf.ln()

    pdf.output(output_path)

def merge_pdfs(original_pdf, extra_page_pdf, output_pdf_path):
    merger = PdfMerger()
    merger.append(original_pdf)
    merger.append(extra_page_pdf)
    merger.write(output_pdf_path)
    merger.close()

def main():
    st.title("Procesamiento")

    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "show_saved" not in st.session_state:
        st.session_state.show_saved = False

    uploaded_file = st.file_uploader("Subir archivo .pdf", type=["pdf"])
    if uploaded_file is not None and not st.session_state.processed:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name
            st.session_state.temp_path = temp_path  # ✅ AGREGADO

        with st.spinner("Procesando archivo..."):
            extracted_data = process_pdf(temp_path)
            extracted_data.setdefault('text_fields', {
                'resultados': '',
                'conclusiones': '',
                'recomendaciones': ''
            })
            extracted_data.setdefault('plots', [[], []])

            st.session_state.extracted_data = extracted_data
            st.session_state.processed = True

    if st.session_state.extracted_data:
        extracted_data = st.session_state.extracted_data
        display_tables(extracted_data)

        st.subheader("Secciones finales")
        text_fields = extracted_data.get('text_fields', {})
        resultados = st.text_area("Resultados (solo editable por el usuario)", text_fields.get('resultados', ''), key="resultados_edit")
        conclusiones = st.text_area("Conclusiones", text_fields.get('conclusiones', ''), key="conclusiones_edit")
        recomendaciones = st.text_area("Recomendaciones", text_fields.get('recomendaciones', ''), key="recomendaciones_edit")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generar Conclusiones con AI"):
                with st.spinner("Generando conclusiones..."):
                    nuevas_conclusiones = generate_text(extracted_data['quantitative_data'], resultados, 'conclusiones')
                    st.session_state.extracted_data['text_fields']['conclusiones'] = nuevas_conclusiones
                    st.rerun()
        with col2:
            if st.button("Generar Recomendaciones con AI"):
                with st.spinner("Generando recomendaciones..."):
                    nuevas_recomendaciones = generate_text(extracted_data['quantitative_data'], resultados, 'recomendaciones')
                    st.session_state.extracted_data['text_fields']['recomendaciones'] = nuevas_recomendaciones
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            if st.button("Guardar cambios"):
                # Actualizamos todos los campos que deben persistirse
                st.session_state.extracted_data['text_fields'] = {
                    'resultados': resultados,
                    'conclusiones': conclusiones,
                    'recomendaciones': recomendaciones
                }

                mongo_id = extracted_data.get("_id")
                if not mongo_id:
                    st.error("No se encontró el ID del documento en MongoDB.")
                else:
                    update_fields = {
                        "text_fields": st.session_state.extracted_data["text_fields"],
                        "quantitative_data": st.session_state.extracted_data["quantitative_data"],
                        "patient_data": st.session_state.extracted_data["patient_data"]
                    }

                    updated = mongo_manager.update_document_by_id(
                        collection_name=MONGO_COLLECTION,
                        document_id=mongo_id,
                        update_fields=update_fields
                    )

                    if updated:
                        st.success("Cambios guardados correctamente en MongoDB.")
                        st.session_state.show_saved = True
                    else:
                        st.warning("No se realizaron cambios o hubo un problema al guardar.")

        with col_btn2:
            if st.button("Borrar cambios"):
                st.warning("Funcionalidad en desarrollo.")
        
        with col_btn3:
            uploaded_file_id = None  # ← Definimos la variable antes del bloque
            if st.button("Descargar informe"):
                with st.spinner("Generando informe PDF actualizado..."):
                    # Paso 1: Crear PDF con los campos textuales
                    temp_dir = tempfile.mkdtemp()
                    text_fields_path = os.path.join(temp_dir, "text_fields.pdf")
                    final_pdf_path = os.path.join(temp_dir, "updated_report.pdf")

                    create_text_fields_pdf({
                      'resultados': resultados,
                      'conclusiones': conclusiones,
                      'recomendaciones': recomendaciones
                    }, text_fields_path)

                    # Paso 2: Obtener el PDF original cargado
                    #original_pdf_path = temp_path  # se definió arriba cuando se sube el archivo
                    original_pdf_path = st.session_state.get("temp_path")  # ✅ CAMBIO

                    if not original_pdf_path:
                        st.error("No se encontró el archivo PDF original. Por favor, vuelve a subirlo.")
                    else:
                        merge_pdfs(original_pdf_path, text_fields_path, final_pdf_path)
                    # Paso 3: Combinar original + hoja de texto
                    #merge_pdfs(original_pdf_path, text_fields_path, final_pdf_path)

                    # Paso 4: Subir a Google Drive
                    uploader = Uploader()
                    folder_id = os.getenv("GDRIVE_REPORTS_FOLDER_ID")  # usa tu carpeta específica
                    uploaded_file_id = uploader.upload_file(final_pdf_path, folder_id)

            if uploaded_file_id:
                drive_link = f"https://drive.google.com/file/d/{uploaded_file_id}/view"
                st.success("Informe actualizado subido a Google Drive.")
                st.markdown(f"📄 [Ver PDF en Google Drive]({drive_link})")
            else:
                st.error("Hubo un error al subir el informe a Google Drive.")
      

        if st.session_state.show_saved:
            st.markdown("<h3 style='text-align: center;'>Datos guardados en MongoDB</h3>", unsafe_allow_html=True)
            df_guardado = pd.DataFrame({
                "Campo": list(st.session_state.extracted_data['text_fields'].keys()),
                "Valor": list(st.session_state.extracted_data['text_fields'].values())
            })
            st.table(df_guardado)

        st.subheader("Gráficos")
        image_list = extracted_data.get('plots', [[], []])[1]
        image_carousel(image_list)

    else:
        st.info("No hay datos extraídos aún. Por favor, sube un archivo PDF para procesar.")

if __name__ == "__main__":
    main()

######################################################################################################################################################################
# # #En este ya funciona bien "Guardar cambios"
# import os
# import sys
# import tempfile
# import streamlit as st
# import pandas as pd

# # Agrega el directorio principal al path del sistema para importar módulos correctamente
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# # Importa funciones y clases necesarias
# from src.main_extraction import process_file
# from src.generate_sections.main import write_report_from_data
# from src.common.mongo_manager import MongoManager

# MONGO_URI = os.getenv('MONGO_URI')
# MONGO_DATABASE = os.getenv('MONGO_DATABASE')
# MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

# # Configura la página en Streamlit
# st.set_page_config(page_title="Procesamiento", layout="wide")

# # Inicializa la conexión con la base de datos
# mongo_manager = MongoManager(MONGO_URI, MONGO_DATABASE)

# @st.cache_data
# def process_pdf(file_path):
#     return process_file(file_path)

# def generate_text(data, results, text_type):
#     return write_report_from_data(data, results, text_type)

# def image_carousel(image_list):
#     if image_list:
#         selected_image = st.slider("Carousel", 0, len(image_list) - 1, 0, format="Imagen %d")
#         st.image(image_list[selected_image], use_column_width=True, caption=f"Imagen {selected_image + 1}")
#     else:
#         st.write("No hay imágenes para mostrar.")

# def display_tables(extracted_data):
#     st.markdown("<h3 style='text-align: center;'>Datos personales del paciente</h3>", unsafe_allow_html=True)
#     df_patient = pd.DataFrame({k: [v] for k, v in extracted_data['patient_data'].items()})
#     edited_patient = st.data_editor(df_patient, use_container_width=True, key="df_patient")

#     st.markdown("<h3 style='text-align: center;'>Datos cuantitativos del paciente</h3>", unsafe_allow_html=True)
#     df_quant = pd.DataFrame({k: [v] for k, v in extracted_data['quantitative_data'].items()})
#     edited_quant = st.data_editor(df_quant, use_container_width=True, key="df_quant")

#     extracted_data['patient_data'] = edited_patient.to_dict(orient='records')[0]
#     extracted_data['quantitative_data'] = edited_quant.to_dict(orient='records')[0]

# def main():
#     st.title("Procesamiento")

#     if "extracted_data" not in st.session_state:
#         st.session_state.extracted_data = None
#     if "processed" not in st.session_state:
#         st.session_state.processed = False
#     if "show_saved" not in st.session_state:
#         st.session_state.show_saved = False

#     uploaded_file = st.file_uploader("Subir archivo .pdf", type=["pdf"])
#     if uploaded_file is not None and not st.session_state.processed:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#             tmp_file.write(uploaded_file.read())
#             temp_path = tmp_file.name

#         with st.spinner("Procesando archivo..."):
#             extracted_data = process_pdf(temp_path)
#             extracted_data.setdefault('text_fields', {
#                 'resultados': '',
#                 'conclusiones': '',
#                 'recomendaciones': ''
#             })
#             extracted_data.setdefault('plots', [[], []])

#             st.session_state.extracted_data = extracted_data
#             st.session_state.processed = True

#     if st.session_state.extracted_data:
#         extracted_data = st.session_state.extracted_data
#         display_tables(extracted_data)

#         st.subheader("Secciones finales")
#         text_fields = extracted_data.get('text_fields', {})
#         resultados = st.text_area("Resultados", text_fields.get('resultados', ''), key="resultados_edit")
#         conclusiones = st.text_area("Conclusiones", text_fields.get('conclusiones', ''), key="conclusiones_edit")
#         recomendaciones = st.text_area("Recomendaciones", text_fields.get('recomendaciones', ''), key="recomendaciones_edit")

#         col1, col2, col3 = st.columns(3)
#         with col2:
#             if st.button("Generar Conclusiones con AI"):
#                 with st.spinner("Generando conclusiones..."):
#                     nuevas_conclusiones = generate_text(extracted_data['quantitative_data'], resultados, 'conclusiones')
#                     st.session_state.extracted_data['text_fields']['conclusiones'] = nuevas_conclusiones
#                     st.rerun()
#         with col3:
#             if st.button("Generar Recomendaciones con AI"):
#                 with st.spinner("Generando recomendaciones..."):
#                     nuevas_recomendaciones = generate_text(extracted_data['quantitative_data'], resultados, 'recomendaciones')
#                     st.session_state.extracted_data['text_fields']['recomendaciones'] = nuevas_recomendaciones
#                     st.rerun()

#         st.markdown("<hr>", unsafe_allow_html=True)
#         col_btn1, col_btn2, col_btn3 = st.columns(3)

#         with col_btn1:
#             if st.button("Guardar cambios"):
#                 st.session_state.extracted_data['text_fields'] = {
#                     'resultados': resultados,
#                     'conclusiones': conclusiones,
#                     'recomendaciones': recomendaciones
#                 }

#                 mongo_id = extracted_data.get("_id")
#                 if not mongo_id:
#                     st.error("No se encontró el ID del documento en MongoDB.")
#                 else:
#                     updated = mongo_manager.update_document_by_id(
#                         collection_name=MONGO_COLLECTION,
#                         document_id=mongo_id,
#                         update_fields={"text_fields": st.session_state.extracted_data["text_fields"]}
#                     )

#                     if updated:
#                         st.success("Cambios guardados correctamente en MongoDB.")
#                         st.session_state.show_saved = True
#                     else:
#                         st.warning("No se realizaron cambios o hubo un problema al guardar.")

#         with col_btn2:
#             if st.button("Borrar cambios"):
#                 st.warning("Funcionalidad en desarrollo.")
#         with col_btn3:
#             if st.button("Descargar"):
#                 st.warning("Funcionalidad en desarrollo.")

#         if st.session_state.show_saved:
#             st.markdown("<h3 style='text-align: center;'>Datos guardados en MongoDB</h3>", unsafe_allow_html=True)
#             df_guardado = pd.DataFrame({
#                 "Campo": list(st.session_state.extracted_data['text_fields'].keys()),
#                 "Valor": list(st.session_state.extracted_data['text_fields'].values())
#             })
#             st.table(df_guardado)

#         st.subheader("Gráficos")
#         image_list = extracted_data.get('plots', [[], []])[1]
#         image_carousel(image_list)

#     else:
#         st.info("No hay datos extraídos aún. Por favor, sube un archivo PDF para procesar.")

# if __name__ == "__main__":
#     main()

##############################################################################################
#--------------------------------------------------------------------
# import os
# import sys
# import tempfile
# import streamlit as st
# import pandas as pd
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# from src.main_extraction import process_file
# from src.generate_sections.main import write_report_from_data

# # Configure the page
# st.set_page_config(page_title="Procesamiento", layout="wide")

# # Cache the file processing to avoid unnecessary reprocessing
# @st.cache_data
# def process_pdf(file_path):
#     return process_file(file_path)

# def generate_text(data,results, text_type):
#     """Generate new text (resultados, conclusiones, recomendaciones) using AI."""
#     return write_report_from_data(data,results, text_type)

# def image_carousel(image_list):
#     """Displays an image carousel given a list of image paths."""
#     if image_list:
#         selected_image = st.slider("Carousel", 0, len(image_list) - 1, 0, format="Image %d")
#         st.image(image_list[selected_image], use_column_width=True, caption=f"Image {selected_image + 1}")
#     else:
#         st.write("No images available to display.")

# def display_tables(extracted_data):
#     """Display the extracted patient and quantitative data in editable tables."""
#     st.markdown("<h3 style='text-align: center;'>Datos personales del paciente</h3>", unsafe_allow_html=True)
#     df_patient = pd.DataFrame({k: [v] for k, v in extracted_data['patient_data'].items()})
#     # Use the data editor so users can modify patient data directly
#     edited_patient = st.data_editor(df_patient, use_container_width=True, key="df_patient")
    
#     st.markdown("<h3 style='text-align: center;'>Datos cuantitativos del paciente</h3>", unsafe_allow_html=True)
#     df_quant = pd.DataFrame({k: [v] for k, v in extracted_data['quantitative_data'].items()})
#     # Use the data editor for quantitative data
#     edited_quant = st.data_editor(df_quant, use_container_width=True, key="df_quant")
    
#     # Optionally, update the extracted_data with edited values
#     extracted_data['patient_data'] = edited_patient.to_dict(orient='records')[0]
#     extracted_data['quantitative_data'] = edited_quant.to_dict(orient='records')[0]


# def main():
#     st.title("Procesamiento")
    
#     # Initialize session state flags if not set
#     if "extracted_data" not in st.session_state:
#         st.session_state.extracted_data = None
#     if "processed" not in st.session_state:
#         st.session_state.processed = False

#     # File upload
#     uploaded_file = st.file_uploader("Subir archivo.pdf", type=["pdf"])
#     if uploaded_file is not None and not st.session_state.processed:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#             tmp_file.write(uploaded_file.read())
#             temp_path = tmp_file.name

#         with st.spinner("Processing file..."):
#             extracted_data = process_pdf(temp_path)
#             st.session_state.extracted_data = extracted_data
#             st.session_state.processed = True  # Mark file as processed

#     if st.session_state.extracted_data:
#         extracted_data = st.session_state.extracted_data

#         # Display extracted data in two columns
#         # col1, col2 = st.columns([1, 3])
#         # with col1:
#         display_tables(extracted_data)
#         # with col2:
#         # Display text areas for results, conclusions, and recommendations
#         st.subheader("Secciones finales")
#         resultados = st.text_area("Resultados", extracted_data['text_fields'].get('resultados', ''))
#         conclusiones = st.text_area("Conclusiones", extracted_data['text_fields'].get('conclusiones', ''))
#         recomendaciones = st.text_area("Recomendaciones", extracted_data['text_fields'].get('recomendaciones', ''))

#         col1, col2, col3 = st.columns(3)
#         # Buttons for regenerating text with AI, without triggering pdf reprocessing
#         # with col1:
#         #     if st.button("Generar Resultados con AI"):
#         #         with st.spinner("Generando resultados..."):
#         #             nuevos_resultados = generate_text(extracted_data['quantitative_data'],extracted_data['text_fields']['resultados'], 'resultados')
#         #             st.session_state.extracted_data['text_fields']['resultados'] = nuevos_resultados
#         #             st.experimental_rerun()  # Update UI with new text
#         with col2:
#             if st.button("Generar Conclusiones con AI"):
#                 with st.spinner("Generando conclusiones..."): #Check si funciona bien
#                     nuevas_conclusiones = generate_text(extracted_data['quantitative_data'],extracted_data['text_fields']['resultados'], 'conclusiones')
#                     st.session_state.extracted_data['text_fields']['conclusiones'] = nuevas_conclusiones
#                     st.experimental_rerun()
#         with col3:
#             if st.button("Generar Recomendaciones con AI"):
#                 with st.spinner("Generando recomendaciones..."): #Check si funciona bien
#                     nuevas_recomendaciones = generate_text(extracted_data['quantitative_data'],extracted_data['text_fields']['resultados'], 'recomendaciones')
#                     st.session_state.extracted_data['text_fields']['recomendaciones'] = nuevas_recomendaciones
#                     st.experimental_rerun()

#         # Additional action buttons (e.g., Guardar, Borrar cambios, Descargar)
#         st.markdown("<hr>", unsafe_allow_html=True)
#         col_btn1, col_btn2, col_btn3 = st.columns(3)
#         with col_btn1:
#             if st.button("Guardar"):
#                 st.write("Guardando!")  # Implement save logic here
#         with col_btn2:
#             if st.button("Borrar cambios"):
#                 st.write("Borrar triggered!")  # Implement cancel/reset logic here
#         with col_btn3:
#             if st.button("Descargar"):
#                 st.write("Descargando!")  # Implement download logic here

#         # Display image carousel for plots
#         st.subheader("Gráficos")
#         image_list = extracted_data['plots'][1] #'example_data/plots'
#         print(f"plot dir {image_list}")
#         # if os.path.exists(plot_dir):
#             # image_list = #[os.path.join(plot_dir, plot) for plot in os.listdir(plot_dir)]
#         image_carousel(image_list)
#         # else:
#         #     st.write("No plots directory found.")
#     else:
#         st.write("No data extracted yet. Please upload a file to see data.")

# if __name__ == "__main__":
#     main()
