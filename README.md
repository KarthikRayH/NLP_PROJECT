# Natural Language Processing (NLP) Chatbot

[![Python Versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-Flask%20%26%20scikit--learn-orange.svg)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](test_chatbot.py)

An educational, rule-and-similarity based **NLP Chatbot** built in Python with **Flask** and **scikit-learn**.

This project demonstrates the classic foundational Natural Language Processing (NLP) pipeline without relying on external APIs or heavyweight neural models. It is lightweight, inspectable, fast, and ideal for academic demonstrations, assignments, and viva presentations.

---

## 🎯 How It Works: The NLP Pipeline

```
User Input ("Explain TF-IDF")
         │
         ▼
[1. Text Normalization]  ──► Lowercase, remove special characters & punctuation
         │
         ▼
[2. Tokenization]        ──► Split into word tokens: ['explain', 'tf', 'idf']
         │
         ▼
[3. Stop Word Removal]   ──► Remove non-informative words ('is', 'the', etc.)
         │
         ▼
[4. TF-IDF Vector Space] ──► Transform tokens into numerical weight vectors (Unigrams + Bigrams)
         │
         ▼
[5. Cosine Similarity]   ──► Compute similarity against all pre-trained intent patterns
         │
         ▼
[6. Confidence Threshold]──► If score >= 0.20: Return intent response
                             If score < 0.20:  Return polite fallback guidance
```

### Key NLP Concepts Applied

1. **Text Normalization:** Converts text to lowercase to make `"Hello"`, `"HELLO"`, and `"hello"` identical, and strips punctuation.
2. **Tokenization:** Breaks the normalized sentence into individual words/tokens for analysis.
3. **Stop Word Filtering:** Discards frequent words with minimal distinguishing meaning (e.g., `'the'`, `'is'`, `'at'`) while preserving key domain acronyms like `'nlp'`, `'ai'`, and `'ml'`.
4. **TF-IDF (Term Frequency-Inverse Document Frequency):** Converts text into multi-dimensional vectors where terms that are unique and descriptive receive higher weights than ubiquitous terms.
5. **Cosine Similarity:** Measures the angle between the user query vector and candidate training patterns in the vector space (ranging from `0.0` for orthogonal/unrelated to `1.0` for identical).
6. **Fallback Mechanism:** Handles out-of-scope or low-confidence questions gracefully.

---

## 📂 Project Structure

```
NLP/
├── .github/
│   ├── workflows/
│   │   └── ci.yml              # GitHub Actions automated test matrix
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml      # GitHub issue template for bugs
│   │   └── feature_request.yml # GitHub issue template for new intents
│   └── PULL_REQUEST_TEMPLATE.md# Pull request template checklist
├── data/
│   └── intents.json            # Knowledge base containing tags, patterns, and responses
├── static/
│   ├── script.js               # Client-side JavaScript handling chat interactions
│   └── style.css               # Responsive, modern glassmorphic interface styles
├── templates/
│   └── index.html              # Accessible HTML5 web interface
├── .gitignore                  # Git ignore rules for Python, IDEs, and OS files
├── app.py                      # Flask server and REST API endpoints (/api/chat, /api/health)
├── chatbot.py                  # Core NLP engine class & standalone CLI chat runner
├── CONTRIBUTING.md             # Contribution guidelines & intent authoring guide
├── LICENSE                     # MIT Open Source License
├── requirements.txt            # Project dependencies (Flask, scikit-learn, numpy)
├── test_chatbot.py             # Automated unit test suite
└── README.md                   # Documentation and Viva Voce preparation guide
```

---

## 🚀 Getting Started

### 1. Clone the Repository & Install Dependencies

```bash
git clone https://github.com/<your-username>/NLP.git
cd NLP

# Optional: Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Run in Web Mode (Interactive Web App)

Start the Flask development server:
```bash
python app.py
```
Or specify a custom port:
```bash
python app.py 5001
```

Then open your browser and navigate to:
```
http://127.0.0.1:5001
```

### 3. Run in CLI Mode (Terminal Only)

You can also run the chatbot directly inside your terminal:
```bash
python chatbot.py
```
Type any message or ask about NLP concepts (e.g., `"What is tokenization?"`, `"Explain TF-IDF"`). Type `quit` or `exit` to exit.

### 4. Run Automated Unit Tests

Verify that all preprocessing, vectorization, intent matching, and API endpoints are working properly:
```bash
python -m unittest test_chatbot.py -v
```

---



## 🤝 Contributing

Contributions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new intents, submitting bug reports, and sending pull requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
