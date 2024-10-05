import json
import os
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


def __extract_plots_from_image(images):
    #TODO: completar con el código para recortar plots
    pass