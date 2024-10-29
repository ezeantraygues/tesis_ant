import json
import os
import cv2
import base64
import numpy as np
from typing import List
from typing import List
#from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import AzureOpenAI
#PREGUNTA: 


from models.report import DataExtractorResponse

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_CHAT_DEPLOYMENT_NAME")

from .prompts import USER_TEXT_CONTENT, SYSTEM_CONTENT


chat = AzureOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_CHAT_DEPLOYMENT_NAME,
    openai_api_version="2024-08-01-preview",
    temperature=0.25,
    request_timeout=550,
    max_tokens=4000,
)

system_message = SystemMessage(content=SYSTEM_CONTENT)


def extract_data_from_image(images: List[str]):
    return {
        'data':__extract_data_from_image_llm(images),
        'plots':__extract_plots_from_image(images)
    }


def __extract_data_from_image_llm(
    images: List[str], mime_type: str = "image/jpeg", detail: str = "auto"
) -> DataExtractorResponse:
    """
    Extract document data from images

    Args:
        images (List[str]): List of base64 encoded images
        mime_type (str, optional): MIME type of the image. Defaults to "image/jpeg".
        detail (str, optional): Detail of the image. Defaults to "auto". (high/low/auto)

    Returns:
        List[DocumentData]: List of DocumentData objects extracted from the images
    """

    # Create a HumanMessage with the images
    images_content = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{image}", "detail": detail},
        }
        for image in images
    ]

    user_message = HumanMessage(
        content=[{"type": "text", "text": USER_TEXT_CONTENT}] + images_content
    )

    # Invoke the chat with the system message and the user message
    history = [system_message, user_message]

    # Get the response from the chat
    response = chat.invoke(history, response_format = DataExtractorResponse)

    # Extract the data from the response
    extracted_data = json.loads(response.content)

    return extracted_data


# def __extract_plots_from_image(images):
    #TODO: completar con el código para recortar plots

# def __extract_plots_from_image(images: List[str]):
#     """
#     Extrae gráficos (plots) de las imágenes proporcionadas.

#     Args:
#         images (List[str]): Lista de imágenes codificadas en base64.

#     Returns:
#         List[np.ndarray]: Lista de imágenes recortadas que contienen los gráficos.
#     """
#     plots = []  # Lista para almacenar los gráficos recortados

#     for img_base64 in images:
#         # Decodifica la imagen base64
#         img_array = np.frombuffer(base64.b64decode(img_base64), dtype=np.uint8)
#         image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#         # Convertir la imagen a escala de grises
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#         # Aplicar un desenfoque para reducir el ruido
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#         # Detectar bordes utilizando Canny
#         edged = cv2.Canny(blurred, 50, 150)

#         # Encontrar contornos
#         contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         for contour in contours:
#             # Obtener el área delimitada por el contorno
#             x, y, w, h = cv2.boundingRect(contour)

#             # Filtrar contornos pequeños para evitar recortes irrelevantes
#             if w > 50 and h > 50:
#                 # Recortar la imagen al área del gráfico
#                 plot = image[y:y+h, x:x+w]
#                 plots.append(plot)  # Agregar el gráfico recortado a la lista

#     return plots  # Devolver la lista de gráficos recortados


#     pass
def __extract_plots_from_image(images: List[np.ndarray]):
    """
    Extrae gráficos (plots) de las imágenes proporcionadas.

    Args:
        images (List[np.ndarray]): Lista de imágenes en formato np.ndarray (ya preprocesadas).

    Returns:
        List[np.ndarray]: Lista de imágenes recortadas que contienen los gráficos.
    """
    plots = []  # Lista para almacenar los gráficos recortados

    for image in images:
        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicar un desenfoque para reducir el ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detectar bordes utilizando Canny
        edged = cv2.Canny(blurred, 50, 150)

        # Encontrar contornos
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Obtener el área delimitada por el contorno
            x, y, w, h = cv2.boundingRect(contour)

            # Filtrar contornos pequeños para evitar recortes irrelevantes
            if w > 50 and h > 50:
                # Recortar la imagen al área del gráfico
                plot = image[y:y+h, x:x+w]
                plots.append(plot)  # Agregar el gráfico recortado a la lista

    return plots  # Devolver la lista de gráficos recortados
