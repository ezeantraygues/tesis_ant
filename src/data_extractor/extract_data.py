import json
import os
from PIL import Image
import base64
from io import BytesIO
import base64
from typing import List
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


from models.report import DataExtractorResponse

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_CHAT_DEPLOYMENT_NAME")

from .prompts import USER_TEXT_CONTENT, SYSTEM_CONTENT


chat = AzureChatOpenAI(
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

    llm_data = __extract_data_from_image_llm(images)
    return {
        'patient_data': llm_data['patient_data'],
        'quantitative_data': llm_data['quantitative_data'],
        'text_fields': llm_data['text_fields'],
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


def __extract_plots_from_image(images):

    crop_images = []

    #Buscar las coordenadas de cada plot en cada página, en formato left,upper,right,lower
    crop_coordinates = [[],[(35, 540, 955, 960)],[(40, 100, 950, 400),(40, 420, 480, 580),(40, 580, 480, 740),(40, 740, 480, 900),(510, 420, 960, 580),(510, 580, 950, 740),(510, 740, 950, 900)],[(35, 80, 950, 900)],[(35, 80, 950, 900)],[(35, 60, 950, 950)],[],[(35, 160, 950, 950)],[(35, 160, 950, 950)],[],[(35, 160, 950, 950)],[(35, 160, 950, 950)],[]]
    #crop_coordinates = [[],[(rango de rot pelvica)],[(cap de amortiguacion),(dur ciclo de la carr),(cadencia),(vel de propulsion),(ind de simetria),(dur fase contacto),(dur fas apoyo)],[(graficos ciclo correr)],[(graficos ciclo caminar)],[(dinamica musculos)],[],[(prueba salto rig bipodlico)],[(prueba salto rig bipodlico))],[],[(prueba salto rig monopodlico)],[(prueba salto rig monopodlico)],[]]
    # podria dividir en 4 el de dinamica musculos (corchete nro 6) 
    for idx,image in enumerate(images):
        # Convert the base64 string back to bytes
        image_data = base64.b64decode(image)

        # Load the image from bytes
        image = Image.open(BytesIO(image_data))

        # Define the coordinates for cropping (left, upper, right, lower)
        # Example coordinates, change them to the desired ones
        for coordinate in crop_coordinates[idx]:
            left, upper, right, lower = coordinate
            
            # Crop the image
            crop_images.append(image.crop((left, upper, right, lower)))
            # cropped_image.save("cropped_image.png")
    return crop_images
# import json
# import os
# from PIL import Image
# import base64
# from io import BytesIO
# import base64
# from typing import List
# from langchain_openai import AzureChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage


# from models.report import DataExtractorResponse

# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_CHAT_DEPLOYMENT_NAME")

# from .prompts import USER_TEXT_CONTENT, SYSTEM_CONTENT


# chat = AzureChatOpenAI(
#     openai_api_key=AZURE_OPENAI_API_KEY,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT,
#     deployment_name=AZURE_CHAT_DEPLOYMENT_NAME,
#     openai_api_version="2024-08-01-preview",
#     temperature=0.25,
#     request_timeout=550,
#     max_tokens=4000,
# )

# system_message = SystemMessage(content=SYSTEM_CONTENT)


# def extract_data_from_image(images: List[str]):

#     llm_data = __extract_data_from_image_llm(images)
#     return {
#         'quantitative_data': llm_data['quantitative_data'],
#         'text_fields': llm_data['text_fields'],
#         'plots':__extract_plots_from_image(images)
#     }


# def __extract_data_from_image_llm(
#     images: List[str], mime_type: str = "image/jpeg", detail: str = "auto"
# ) -> DataExtractorResponse:
#     """
#     Extract document data from images

#     Args:
#         images (List[str]): List of base64 encoded images
#         mime_type (str, optional): MIME type of the image. Defaults to "image/jpeg".
#         detail (str, optional): Detail of the image. Defaults to "auto". (high/low/auto)

#     Returns:
#         List[DocumentData]: List of DocumentData objects extracted from the images
#     """

#     # Create a HumanMessage with the images
#     images_content = [
#         {
#             "type": "image_url",
#             "image_url": {"url": f"data:{mime_type};base64,{image}", "detail": detail},
#         }
#         for image in images
#     ]

#     user_message = HumanMessage(
#         content=[{"type": "text", "text": USER_TEXT_CONTENT}] + images_content
#     )

#     # Invoke the chat with the system message and the user message
#     history = [system_message, user_message]

#     # Get the response from the chat
#     response = chat.invoke(history, response_format = DataExtractorResponse)

#     # Extract the data from the response
#     extracted_data = json.loads(response.content)

#     return extracted_data


# def __extract_plots_from_image(images):

#     crop_images = []

#     #Buscar las coordenadas de cada plot en cada página, en formato left,upper,right,lower
#     crop_coordinates = [
#         [(10,10,80,80),(),()], #Pag 1
#         [(),(),()], #Pag 2
#         [], #Pag 3
#         []
#     ]

     
#     for idx,image in enumerate(images):
#         # Convert the base64 string back to bytes
#         image_data = base64.b64decode(image)

#         # Load the image from bytes
#         image = Image.open(BytesIO(image_data))
        
#         with open("image.png", "wb") as file:
#             file.write(image_data)

#         # Define the coordinates for cropping (left, upper, right, lower)
#         # Example coordinates, change them to the desired ones
#         for coordinate in crop_coordinates[idx]:
#             left, upper, right, lower = coordinate
            
#             # Crop the image
#             crop_images.append(image.crop((left, upper, right, lower)))
#             # cropped_image.save("cropped_image.png")
#     return crop_images