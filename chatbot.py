"""Core NLP Chatbot Engine using TF-IDF and Cosine Similarity.

This module implements a classic, transparent Natural Language Processing (NLP)
chatbot pipeline:
1. Text Normalization (lowercase, strip whitespace)
2. Tokenization & Cleaning (punctuation removal)
3. Stopword Filtering (preserving domain keywords like 'ai', 'ml', 'nlp')
4. N-gram TF-IDF Vectorization (unigrams + bigrams)
5. Cosine Similarity Matching against known intent patterns
6. Confidence Thresholding and Fallback Handling
"""

import json
import os
import random
import re
from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class NLPChatbot:
    """A classic TF-IDF and Cosine Similarity based NLP Chatbot."""

    # Retain domain-specific words that general stopword lists might otherwise drop
    PRESERVED_KEYWORDS = {"ai", "ml", "nlp", "bow", "tf", "idf", "n"}

    def __init__(
        self,
        intents_path: Optional[str] = None,
        confidence_threshold: float = 0.20,
    ) -> None:
        """Initialize and train the TF-IDF vectorizer on the intent corpus."""
        if intents_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            intents_path = os.path.join(base_dir, "data", "intents.json")

        self.intents_path = intents_path
        self.confidence_threshold = confidence_threshold

        self.intents_data = self._load_intents()
        self.patterns: List[str] = []
        self.pattern_intent_tags: List[str] = []
        self.responses_by_tag: Dict[str, List[str]] = {}

        self._prepare_training_data()

        # Vectorizer with unigrams & bigrams for better phrase matching
        self.vectorizer = TfidfVectorizer(
            token_pattern=r"(?u)\b\w+\b",
            ngram_range=(1, 2),
        )
        self.fitted_vectors = self.vectorizer.fit_transform(self.patterns)

    def _load_intents(self) -> Dict[str, Any]:
        """Load intent specifications from JSON file."""
        if not os.path.exists(self.intents_path):
            raise FileNotFoundError(f"Intents file not found: {self.intents_path}")
        with open(self.intents_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _prepare_training_data(self) -> None:
        """Extract and clean patterns and map them to their respective intent tags."""
        for item in self.intents_data.get("intents", []):
            tag = item["tag"]
            self.responses_by_tag[tag] = item.get("responses", [])
            for pattern in item.get("patterns", []):
                cleaned = self.preprocess(pattern)
                if cleaned:
                    self.patterns.append(cleaned)
                    self.pattern_intent_tags.append(tag)

    @classmethod
    def preprocess(cls, text: str) -> str:
        """Clean, normalize, tokenize, and filter stopwords from text.

        Steps:
        1. Lowercase normalization
        2. Replace non-alphanumeric characters with spaces
        3. Tokenize by whitespace
        4. Remove standard stop words while preserving key NLP acronyms
        """
        normalized = text.lower().strip()
        cleaned = re.sub(r"[^a-z0-9\s]", " ", normalized)
        tokens = cleaned.split()

        filtered_tokens = [
            token
            for token in tokens
            if token not in ENGLISH_STOP_WORDS or token in cls.PRESERVED_KEYWORDS
        ]
        return " ".join(filtered_tokens)

    def reply(self, user_message: str) -> Dict[str, Any]:
        """Process a user message and return the matching response with NLP metadata."""
        cleaned = self.preprocess(user_message)
        tokens = cleaned.split() if cleaned else []

        if not cleaned:
            return {
                "response": "Please enter a valid question or message so I can assist you.",
                "intent": "empty_input",
                "confidence": 0.0,
                "tokens": [],
                "matched_pattern": None,
            }

        # Vectorize the incoming cleaned query
        query_vector = self.vectorizer.transform([cleaned])

        # Compute cosine similarity against all known patterns
        similarity_scores = cosine_similarity(query_vector, self.fitted_vectors)[0]
        best_index = int(np.argmax(similarity_scores))
        best_score = float(similarity_scores[best_index])

        # If similarity is below our confidence threshold, trigger fallback
        if best_score < self.confidence_threshold:
            return {
                "response": (
                    "I'm not sure I understand that yet. You can ask me about NLP topics "
                    "like Tokenization, Stemming, Lemmatization, Stop Words, TF-IDF, or Bag of Words!"
                ),
                "intent": "fallback",
                "confidence": round(best_score, 2),
                "tokens": tokens,
                "matched_pattern": None,
            }

        matched_tag = self.pattern_intent_tags[best_index]
        candidate_responses = self.responses_by_tag.get(
            matched_tag,
            ["I understand what you mean, but I don't have a response configured."],
        )
        selected_response = random.choice(candidate_responses)

        return {
            "response": selected_response,
            "intent": matched_tag,
            "confidence": round(best_score, 2),
            "tokens": tokens,
            "matched_pattern": self.patterns[best_index],
        }


def run_cli() -> None:
    """Run an interactive command-line session for testing the chatbot."""
    print("=" * 60)
    print("🤖 Welcome to the Simple NLP Chatbot (CLI Mode)")
    print("Type your message and press Enter.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 60)

    bot = NLPChatbot()

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"quit", "exit", "q"}:
                print("Bot: Goodbye! Have a great day!")
                break

            result = bot.reply(user_input)
            conf_pct = int(result["confidence"] * 100)
            print(f"Bot: {result['response']}")
            print(f"     [Intent: {result['intent']} | Confidence: {conf_pct}%]")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chatbot. Goodbye!")
            break


if __name__ == "__main__":
    run_cli()
