from src.preprocessing.preprocess_files import DataPreprocessor
from src.data_extractor.extract_data import __extract_plots_from_image

def main():
    # Ruta al PDF de prueba
    pdf_path = '00417- 24- CIRILLO Mercedez-.pdf'

    # Leer el contenido del PDF
    with open(pdf_path, 'rb') as file:
        pdf_content = file.read()

    # Convertir PDF a imágenes codificadas en base64
    preprocessor = DataPreprocessor(pdf_content)
    images_base64 = preprocessor()

    # Verificar si las imágenes se procesaron correctamente
    print(f"Número de imágenes procesadas: {len(images_base64)}")
    if not images_base64:
        print("Error: No se generaron imágenes a partir del PDF.")
        return

    # Probar la función de extracción de gráficos
    cropped_images = __extract_plots_from_image(images_base64)

    if not cropped_images:
        print("Error: No se detectaron gráficos en las imágenes procesadas.")
        return

    # Guardar las imágenes recortadas para verificación
    for idx, cropped_img in enumerate(cropped_images):
        cropped_img.save(f"cropped_image_{idx}.png")

    print(f"{len(cropped_images)} imágenes recortadas guardadas.")

if __name__ == "__main__":
    main()


# from dotenv import load_dotenv
# import os
# from src.preprocessing.preprocess_files import DataPreprocessor
# from src.data_extractor.extract_data import __extract_plots_from_image

# # Cargar las variables de entorno
# load_dotenv(dotenv_path='.env.dev')

# def main():
#     # Verificar si las credenciales están cargadas correctamente
#     api_key = os.getenv('AZURE_OPENAI_API_KEY')
#     endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

#     if not api_key or not endpoint:
#         raise EnvironmentError("Faltan las variables de entorno AZURE_OPENAI_API_KEY o AZURE_OPENAI_ENDPOINT.")

#     print(f"API Key cargada: {api_key[:5]}...")  # Imprimir los primeros caracteres de la API Key
#     print(f"Endpoint cargado: {endpoint}")

#     # Ruta al PDF de prueba
#     pdf_path = '00417- 24- CIRILLO Mercedez-.pdf'

#     # Leer el contenido del PDF
#     with open(pdf_path, 'rb') as file:
#         pdf_content = file.read()

#     # Convertir PDF a imágenes codificadas en base64
#     preprocessor = DataPreprocessor(pdf_content)
#     images_base64 = preprocessor()

#     # Probar la función de extracción de gráficos
#     cropped_images = __extract_plots_from_image(images_base64)

#     # Guardar las imágenes recortadas para verificación
#     for idx, cropped_img in enumerate(cropped_images):
#         cropped_img.save(f"cropped_image_{idx}.png")

#     print(f"{len(cropped_images)} imágenes recortadas guardadas.")

# if __name__ == "__main__":
#     main()

#-----------------------------------------------------------------------------------------------------------------
# from src.preprocessing.preprocess_files import DataPreprocessor
# from src.data_extractor.extract_data import __extract_plots_from_image

# def main():
#     # Ruta al PDF de prueba
#     pdf_path = '00417- 24- CIRILLO Mercedez-.pdf'

#     # Leer el contenido del PDF
#     with open(pdf_path, 'rb') as file:
#         pdf_content = file.read()

#     # Convertir PDF a imágenes codificadas en base64
#     preprocessor = DataPreprocessor(pdf_content)
#     images_base64 = preprocessor()

#     # Probar la función de extracción de gráficos
#     cropped_images = __extract_plots_from_image(images_base64)

#     # Guardar las imágenes recortadas para verificación
#     for idx, cropped_img in enumerate(cropped_images):
#         cropped_img.save(f"cropped_image_{idx}.png")

#     print(f"{len(cropped_images)} imágenes recortadas guardadas.")

# if __name__ == "__main__":
#     main()



