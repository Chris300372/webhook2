import json
import os
import openai

# Load OpenAI key from env
openai.api_key = os.getenv("CHATGPT_API_KEY")

# Load knowledge base
KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
with open(KB_PATH, "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)


def search_kb(user_message: str) -> dict:
    """
    Encuentra qué secciones de la base de conocimiento
    son relevantes para la consulta del usuario.
    Heurística simple: compara keywords y palabras.
    """
    matched_sections = {}
    user_lower = user_message.lower()

    # Search by keys and content
    for key, value in KNOWLEDGE.items():
        text_value = json.dumps(value).lower()
        # match if any keyword in key or any word in user message in text_value
        if any(k in user_lower for k in key.split("_")):
            matched_sections[key] = value
        else:
            for word in user_lower.split():
                if len(word) > 3 and word in text_value:
                    matched_sections[key] = value
                    break

    if not matched_sections:
        matched_sections["general"] = KNOWLEDGE.get("general", "")

    return matched_sections


def ai_answer(user_message: str) -> str:
    """
    Genera una respuesta usando ChatGPT + fragmentos relevantes de KB.
    """
    relevant = search_kb(user_message)

    system_prompt = (
        "Eres un asistente profesional del Hotel Mirador & Spa Premium. "
        "Responde de forma amable, clara y en tono humano. Si te preguntan precios, servicios o habitaciones, "
        "usa SOLO la información de la base de conocimiento proporcionada. "
        "Si la pregunta excede la base de conocimiento, indícalo y ofrece contactar al staff."
    )

    # We include the relevant KB fragments concisely
    kb_fragment = json.dumps(relevant, ensure_ascii=False, indent=2)

    user_prompt = f"""Consulta del cliente:
\"\"\"{user_message}\"\"\"

Fragmentos relevantes de la base de conocimiento:
{kb_fragment}

Responde solo en español. No inventes información fuera de la base.
"""

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.15,
            max_tokens=500
        )
        # Defensive parsing
        data = resp
        if isinstance(data, dict) and "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"].strip()
        else:
            print("Respuesta inesperada de OpenAI:", data)
            return "Lo siento, no pude generar la respuesta correctamente. Por favor inténtalo de nuevo."
    except Exception as e:
        print("Error generando respuesta:", e)
        return "Lo siento, hubo un problema al procesar tu consulta. Intenta nuevamente más tarde."
