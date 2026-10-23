"""Automated test suite for the NLP Chatbot."""

import unittest
from app import app
from chatbot import NLPChatbot


class NLPChatbotTests(unittest.TestCase):
    """Test cases for the core NLP pipeline and Flask endpoints."""

    def setUp(self):
        self.bot = NLPChatbot()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_preprocessing(self):
        """Verify normalization, lowercase, punctuation removal, and stop words."""
        raw = "Hello! What is Natural Language Processing???"
        cleaned = self.bot.preprocess(raw)
        self.assertIn("natural", cleaned)
        self.assertIn("language", cleaned)
        self.assertIn("processing", cleaned)
        # Verify punctuation removed
        self.assertNotIn("!", cleaned)
        self.assertNotIn("?", cleaned)

    def test_keyword_preservation(self):
        """Verify key NLP acronyms like 'nlp', 'ai', 'ml' are preserved."""
        cleaned = self.bot.preprocess("Explain what is AI and ML in NLP")
        self.assertIn("ai", cleaned)
        self.assertIn("ml", cleaned)
        self.assertIn("nlp", cleaned)

    def test_greeting_intent(self):
        """Check that standard greetings match the greeting intent."""
        result = self.bot.reply("Hello there")
        self.assertEqual(result["intent"], "greeting")
        self.assertGreaterEqual(result["confidence"], 0.20)

    def test_nlp_concept_intent(self):
        """Check that technical queries match the intended concepts."""
        result = self.bot.reply("Explain what is TF-IDF")
        self.assertEqual(result["intent"], "tfidf")
        self.assertGreaterEqual(result["confidence"], 0.50)

    def test_fallback_intent(self):
        """Check that unknown or unrelated queries trigger the fallback response."""
        result = self.bot.reply("how to bake sourdough bread at home")
        self.assertEqual(result["intent"], "fallback")
        self.assertIn("I'm not sure", result["response"])

    def test_empty_input(self):
        """Check that empty or whitespace strings are handled gracefully."""
        result = self.bot.reply("   ")
        self.assertEqual(result["intent"], "empty_input")

    def test_api_chat_endpoint_valid(self):
        """Test POST /api/chat with valid payload."""
        response = self.client.post("/api/chat", json={"message": "What is tokenization?"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["intent"], "tokenization")
        self.assertIn("response", data)

    def test_api_chat_endpoint_empty(self):
        """Test POST /api/chat with empty payload rejects with 400."""
        response = self.client.post("/api/chat", json={"message": ""})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_api_health_endpoint(self):
        """Test GET /api/health."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "online")
        self.assertGreater(data["intents_loaded"], 0)


if __name__ == "__main__":
    unittest.main()
