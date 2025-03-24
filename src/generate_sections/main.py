
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from models.sections import SectionText
from .prompts import SYSTEM_CONTENT_CONCLUSIONES, USER_MESSAGE_CONCLUSIONES, USER_MESSAGE_RESULTADOS, SYSTEM_CONTENT_RESULTADOS, USER_MESSAGE_RECOMENDACIONES, SYSTEM_CONTENT_RECOMENDACIONES

chat = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    request_timeout=550,
    max_tokens=4000,
)

def write_report_from_data(data: dict, section:str):
    """
    Write a biomechanical report from the extracted data.

    Args:
        data (dict): Extracted data from the images.
    """

    if section == "resultados":
        system_message = SystemMessage(content=SYSTEM_CONTENT_RESULTADOS)
        user_message = HumanMessage(content=USER_MESSAGE_RESULTADOS.format(user_data=data))

    if section == "conclusiones":
        system_message = SystemMessage(content=SYSTEM_CONTENT_CONCLUSIONES)
        user_message = HumanMessage(content=USER_MESSAGE_CONCLUSIONES.format(user_data=data))

    if section == "recomendaciones":
        system_message = SystemMessage(content=SYSTEM_CONTENT_RECOMENDACIONES)
        user_message = HumanMessage(content=USER_MESSAGE_RECOMENDACIONES.format(user_data=data))

    history = [system_message, user_message]
    response = chat.invoke(history, response_format=SectionText)
    return json.loads(response.content)['section']
