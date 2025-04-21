import random
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from models.sections import SectionText
#from .prompts import SYSTEM_CONTENT_CONCLUSIONES, USER_MESSAGE_CONCLUSIONES, USER_MESSAGE_RESULTADOS, SYSTEM_CONTENT_RESULTADOS, USER_MESSAGE_RECOMENDACIONES, SYSTEM_CONTENT_RECOMENDACIONES
from .prompts import (
    SYSTEM_CONTENT_CONCLUSIONES, SYSTEM_CONTENT_RECOMENDACIONES,
    generate_user_message_conclusiones, generate_user_message_recomendaciones
)

# Cargamos ejemplos reales desde el jsonl
with open("informes_dataset.jsonl", "r", encoding="utf-8") as f:
    EJEMPLOS = [json.loads(linea) for linea in f if linea.strip()]

chat = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    request_timeout=550,
    max_tokens=4000,
)

def write_report_from_data(data: dict, results:str, section:str):
    """
    Write a biomechanical report from the extracted data.

    Args:
        data (dict): Extracted data from the images.
    """


    if section == "conclusiones":
        system_message = SystemMessage(content=SYSTEM_CONTENT_CONCLUSIONES)
        user_message = HumanMessage(
            content=generate_user_message_conclusiones(
            results=results,
            user_data=data,
            ejemplos=random.sample(EJEMPLOS, 3)
            #ejemplos=EJEMPLOS[:3]  # o usar random.sample(EJEMPLOS, 3)
        )
    )

    if section == "recomendaciones":
        system_message = SystemMessage(content=SYSTEM_CONTENT_RECOMENDACIONES)
        user_message = HumanMessage(
            content=generate_user_message_recomendaciones(
            results=results,
            user_data=data,
            ejemplos=random.sample(EJEMPLOS, 3)
            #ejemplos=EJEMPLOS[:3]
        )
    )


    history = [system_message, user_message]
    response = chat.invoke(history, response_format=SectionText)
    return json.loads(response.content)['section']
#####################################################################################################################
# # Version original
# import json
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage
# from models.sections import SectionText
# from .prompts import SYSTEM_CONTENT_CONCLUSIONES, USER_MESSAGE_CONCLUSIONES, USER_MESSAGE_RESULTADOS, SYSTEM_CONTENT_RESULTADOS, USER_MESSAGE_RECOMENDACIONES, SYSTEM_CONTENT_RECOMENDACIONES


# chat = ChatOpenAI(
#     model="gpt-4o",
#     temperature=0,
#     request_timeout=550,
#     max_tokens=4000,
# )

# def write_report_from_data(data: dict, results:str, section:str):
#     """
#     Write a biomechanical report from the extracted data.

#     Args:
#         data (dict): Extracted data from the images.
#     """

#     # if section == "resultados":
#     #     system_message = SystemMessage(content=SYSTEM_CONTENT_RESULTADOS)
#     #     user_message = HumanMessage(content=USER_MESSAGE_RESULTADOS.format(user_data=data))

#     if section == "conclusiones":
#         system_message = SystemMessage(content=SYSTEM_CONTENT_CONCLUSIONES)
#         user_message = HumanMessage(content=USER_MESSAGE_CONCLUSIONES.format(user_data=data, results = results))

#     if section == "recomendaciones":
#         system_message = SystemMessage(content=SYSTEM_CONTENT_RECOMENDACIONES)
#         user_message = HumanMessage(content=USER_MESSAGE_RECOMENDACIONES.format(user_data=data, results = results))

#     history = [system_message, user_message]
#     response = chat.invoke(history, response_format=SectionText)
#     return json.loads(response.content)['section']
