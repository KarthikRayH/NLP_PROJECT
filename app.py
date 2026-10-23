"""Flask web server for the Simple NLP Chatbot."""

import os
import sys
from flask import Flask, jsonify, render_template, request

from chatbot import NLPChatbot

app = Flask(__name__)
bot = NLPChatbot()


@app.route("/")
def index():
    """Serve the main chat web interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Process incoming chat messages and return the bot's response."""
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()

    if not user_message:
        return jsonify({
            "error": "Message cannot be empty.",
            "response": "Please type a message before sending.",
            "intent": "empty_input",
            "confidence": 0.0,
            "tokens": []
        }), 400

    result = bot.reply(user_message)
    return jsonify(result)


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint confirming bot readiness."""
    return jsonify({
        "status": "online",
        "intents_loaded": len(bot.responses_by_tag),
        "patterns_count": len(bot.patterns)
    })


def get_available_port(preferred_port: int = 5001) -> int:
    """Find a free port starting with preferred_port or environment variable."""
    import socket

    env_port = os.environ.get("PORT")
    if env_port and env_port.isdigit():
        return int(env_port)

    # Check preferred port first, then fallback to subsequent ports if occupied
    for port in range(preferred_port, preferred_port + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return preferred_port


if __name__ == "__main__":
    port = get_available_port()
    # Check if a custom port was supplied via command-line arguments: python app.py 5001
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    print("=" * 60)
    print(f"🚀 NLP Chatbot Web Server starting on: http://127.0.0.1:5001")
    print(f"📊 Intents loaded: {len(bot.responses_by_tag)} | Patterns: {len(bot.patterns)}")
    print("=" * 60)
    app.run(host="127.0.0.1", port=port, debug=True)
