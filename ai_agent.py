import os
from openai import OpenAI

# Cargar la base de conocimiento desde archivo
def load_knowledge_base():
    try:
        with open("base_conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error cargando base de conocimiento: {e}")
        return ""

BASE_CONOCIMIENTO = load_knowledge_base()


def ai_answer(user_message):
    """
    Genera una respuesta usando ChatGPT y la base de conocimiento.
    """

    try:
        # 🔥 CLIENTE INICIALIZADO DENTRO DE LA FUNCIÓN
        # Esto evita errores de Railway cuando no ha cargado todavía las variables.
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            print("❌ ERROR: OPENAI_API_KEY no está definido en Railway")
            return "Error interno: falta la clave de API."

        client = OpenAI(api_key=api_key)

        prompt = f"""
Eres un asistente inteligente de un hotel 4 y 5 estrellas.
Usa únicamente la información de la base de conocimiento.

BASE DE CONOCIMIENTO:
---------------------
{BASE_CONOCIMIENTO}
---------------------

Usuario: {user_message}

Instrucciones:
- Responde como asistente del hotel, en tono amable y profesional.
- Si no existe la información en la base, dilo claramente.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente de un hotel de lujo."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Error generando respuesta:", e)
        return "Lo siento, hubo un problema generando la respuesta."
