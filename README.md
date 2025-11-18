# Hotel Bot (WhatsApp + ChatGPT) - Paquete

Este paquete contiene una plantilla mínima para integrar WhatsApp Business Cloud con ChatGPT usando FastAPI,
sin necesidad de una base de datos vectorial. Usa una base de conocimiento JSON y una heurística ligera
para seleccionar fragmentos relevantes.

## Estructura
- `webhook_server.py` - FastAPI webhook para WhatsApp (verificación GET y recepción POST).
- `ai_agent.py` - Lógica que busca en `knowledge_base.json` y usa OpenAI para generar la respuesta.
- `whatsapp.py` - Envío de mensajes a WhatsApp Business Cloud.
- `knowledge_base.json` - Base de conocimiento del hotel (ejemplo).
- `requirements.txt` - Dependencias.

## Uso rápido
1. Configura las variables de entorno (en Railway u otro hosting):
   - `CHATGPT_API_KEY`
   - `WHATSAPP_TOKEN`
   - `WHATSAPP_PHONE_ID`
   - `VERIFY_TOKEN` (opcional)

2. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Ejecuta localmente:
   ```
   uvicorn webhook_server:app --host 0.0.0.0 --port 8000
   ```

## Notas
- No subas tus claves a GitHub. Usa variables de entorno.
- Ajusta los modelos y parámetros según tu cuenta de OpenAI.
