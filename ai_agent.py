import os
from openai import OpenAI

# Inicializamos el cliente OpenAI con el nuevo SDK
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cargar la base de conocimiento desde un archivo
def load_knowledge_base():
    try:
        with open("base_conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error cargando base de conocimiento: {e}")
        return ""

BASE_CONOCIMIENTO = load_knowledge_base()


def generate_ai_response(user_message):
    """
    Genera la respuesta del agente IA usando ChatGPT
    """

    try:
        prompt = f"""
Eres un asistente inteligente de un hotel de lujo 4 y 5 estrellas.
Usa la siguiente base de conocimiento para responder únicamente con información real.

Base de Conocimiento:
---------------------
{BASE_CONOCIMIENTO}
---------------------

Usuario: {user_message}

Instrucciones:
- Sé claro, amable y profesional.
- Si el usuario hace una pregunta fuera del contexto del hotel,
  responde brevemente y regresa al contexto del hotel.
- Si algo no está en la base de conocimiento, admite que no está disponible.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo eficiente y económico
            messages=[
                {"role": "system", "content": "Eres un asistente experto en atención al cliente de un hotel."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extraemos el texto de la respuesta
        answer = response.choices[0].message.content
        return answer

    except Exception as e:
        print("Error generando respuesta:", e)
        return "Lo siento, hubo un error interno generando la respuesta."


if __name__ == "__main__":
    # Prueba local
    msg = input("Escribe un mensaje: ")
    print(generate_ai_response(msg))
