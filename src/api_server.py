"""
Flask API server for a simplified chat interface.
Receives user messages, forwards them to the GPT-4.1-nano model,
and returns the model's responses.
"""

from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload


# Configuración de GitHub Models vía OpenAI
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"
token = os.environ["GITHUB_TOKEN"]
if not token:
    raise RuntimeError(
        "La variable de entorno GITHUB_TOKEN no está definida. "
        "Por favor, define GITHUB_TOKEN antes de ejecutar el servidor."
    )

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)


# ============================================================================
# HEALTH ENDPOINT
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        JSON with the service status
    """
    return jsonify({
        "status": "healthy",
        "service": "Technical Documentation Generator",
        "version": "1.0.0",
        "supported_formats": [".py", ".js"]
    }), 200


# ============================================================================
# CHAT ENDPOINT
# ============================================================================

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat with the GPT-4.1-nano model.
    """
    # Verifica que el Content-Type sea application/json
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Body no es JSON válido"}), 400

    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Obtener respuesta del modelo usando OpenAI client
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente útil.",
            },
            {
                "role": "user",
                "content": user_message,
            }
        ],
        temperature=1.0,
        top_p=1.0,
        model=model
    )
    
    return jsonify({"response": response.choices[0].message.content}), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500


if __name__ == '__main__':
    # Run in debug mode
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )
