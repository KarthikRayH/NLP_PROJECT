# Contributing to NLP Chatbot

Thank you for your interest in contributing to the NLP Chatbot project! We welcome contributions, whether it's expanding domain concepts, improving the web interface, or refining the pipeline.

---

## 🛠️ Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/NLP.git
   cd NLP
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💡 How to Add New Intents

The chatbot's knowledge base is located in [data/intents.json](file:///Users/karthik/work/NLP/data/intents.json). To add new conversational patterns or NLP topics:

1. Open `data/intents.json`.
2. Add a new intent object with a unique `tag`, a list of training `patterns`, and a selection of `responses`:
   ```json
   {
     "tag": "named_entity_recognition",
     "patterns": [
       "What is NER?",
       "Explain Named Entity Recognition",
       "How does NER work in NLP?"
     ],
     "responses": [
       "Named Entity Recognition (NER) is an information extraction technique that locates and categorizes entities (such as names, dates, organizations, and locations) in unstructured text."
     ]
   }
   ```
3. Test your new intent in CLI mode or with unit tests.

---

## 🧪 Running Tests

Ensure all tests pass before submitting your pull request:
```bash
python -m unittest test_chatbot.py -v
```

If adding new features, please add corresponding test cases to [test_chatbot.py](file:///Users/karthik/work/NLP/test_chatbot.py).

---

## 🚀 Submitting a Pull Request

1. Create a descriptive branch:
   ```bash
   git checkout -b feature/add-ner-intent
   ```
2. Commit your changes with clear commit messages:
   ```bash
   git commit -m "feat: add named entity recognition intent and tests"
   ```
3. Push to your fork and submit a Pull Request to the `main` branch.
