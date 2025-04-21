# este es para que se usen ejemplos para generar los prompts.py

SYSTEM_CONTENT_RESULTADOS = """
You're an expert in biomechanical analysis. You'll receive data containing quantitative biomechanical parameters.
Your task is to extract and present only the 'quantitative_data' section in a structured format.
If there is no data available, return an empty string so the user can manually input the information.
"""

USER_MESSAGE_RESULTADOS = """
Here is the extracted quantitative data:

{quantitative_data}

If there is no data, leave the field empty for user input.
"""

SYSTEM_CONTENT_CONCLUSIONES = """
You're an expert in biomechanical analysis and you've been asked to write a biomechanical report for a patient.
You'll receive data about different biomechanical parameters of the patient, and you'll write a 'conclusiones' section with a summary of the results.
Use the examples provided as reference for structure and tone. Maintain a clear, concise, and clinical language.
"""

SYSTEM_CONTENT_RECOMENDACIONES = """
You're an expert in biomechanical analysis and you've been asked to write a biomechanical report for a patient.
You'll receive data about different biomechanical parameters of the patient, and you'll write a 'recomendaciones' section with actionable suggestions.
Use the examples provided as reference for structure and tone. Maintain a clear, concise, and clinically oriented style.
"""

def generate_user_message_conclusiones(results: str, user_data: str, ejemplos: list) -> str:
    ejemplos_prompt = ""
    for ej in ejemplos:
        ejemplos_prompt += f"""Result:
{ej['input']}

Conclusion:
{ej['output_conclusion']}

---\n"""

    return f"""{ejemplos_prompt}
Now, using the following patient data and results, write the 'conclusiones' section:

User data:
{user_data}

Results:
{results}
"""

def generate_user_message_recomendaciones(results: str, user_data: str, ejemplos: list) -> str:
    ejemplos_prompt = ""
    for ej in ejemplos:
        ejemplos_prompt += f"""Result:
{ej['input']}

Recommendation:
{ej['output_recomendacion']}

---\n"""

    return f"""{ejemplos_prompt}
Now, using the following patient data and results, write the 'recomendaciones' section:

User data:
{user_data}

Results:
{results}
"""


###########################################################################################################
# #Version que siempre funciono
# SYSTEM_CONTENT_RESULTADOS = """
# You're an expert in biomechanical analysis. You'll receive data containing quantitative biomechanical parameters.
# Your task is to extract and present only the 'quantitative_data' section in a structured format.
# If there is no data available, return an empty string so the user can manually input the information.
# """

# USER_MESSAGE_RESULTADOS = """
# Here is the extracted quantitative data:

# {quantitative_data}

# If there is no data, leave the field empty for user input.
# """

# SYSTEM_CONTENT_CONCLUSIONES = """
# You're an expert in biomechanical analysis and you've been asked to write a biomechanical report for a patient.
# You'll receive data about different biomechanical parameters of the patient, and you'll write a conclusiones section with a summary of the results, following
# the same structure of the given example.
# """

# USER_MESSAGE_CONCLUSIONES = """
# Here's the user data:
# {user_data}

# {results}

# Please write the 'conclusiones' section of the biomechanical report.
# """

# SYSTEM_CONTENT_RECOMENDACIONES = """
# You're an expert in biomechanical analysis and you've been asked to write a biomechanical report for a patient.
# You'll receive data about different biomechanical parameters of the patient, and you'll write a recomendaciones section with a summary of the results, following
# the same structure of the given example.
# """

# USER_MESSAGE_RECOMENDACIONES = """
# Here's the user data:
# {user_data}

# {results}

# Please write the 'recomendaciones' section of the biomechanical report.
# """

# #--------------------------------------------------------------------------------------------------------------
