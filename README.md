# 🤖 AI-Powered Text Summarizer

An AI-powered web application that converts lengthy articles into concise, meaningful summaries using a pretrained NLP model.

## 🌐 Live Demo

**Try the application here:**  
https://ai-powered-text-summarizer-767.streamlit.app/

## 📌 Project Overview

The AI-Powered Text Summarizer is a Natural Language Processing (NLP) project designed to reduce reading time by generating concise summaries from longer text.

The application uses a pretrained DistilBART model to understand input text and generate meaningful summaries without training a language model from scratch.

It also provides features to review original articles, generated summaries, maintain summary history, and evaluate summary quality.

## 🎯 Objectives

- Generate concise summaries from textual content.
- Apply a pretrained NLP summarization model.
- Preserve original articles and generated summaries.
- Evaluate summary quality through human review.
- Identify unsupported claims and important omissions.

## ✨ Features

- **AI Text Summarization:** Generate summaries from user-provided articles.
- **Original Text Preservation:** Keep the source article available for comparison.
- **Summary History:** View previously generated summaries.
- **Human Evaluation:** Review coverage, factual consistency, unsupported claims and omissions.
- **Download Option:** Download generated summaries.
- **Interactive Interface:** User-friendly application built using Streamlit.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Hugging Face Transformers | Pretrained NLP model integration |
| DistilBART | Text summarization model |
| PyTorch | Deep learning framework |
| Pandas | Data handling and CSV storage |
| Git & GitHub | Version control and project hosting |
| Streamlit Community Cloud | Application deployment |

## 🧠 Model Information

**Model:** `sshleifer/distilbart-cnn-6-6`

DistilBART is a pretrained transformer-based model used for abstractive text summarization. It generates shorter versions of articles while attempting to preserve their important information.

## 📂 Project Structure

```text
AI-Powered-Text-Summarizer/
│
├── app.py
├── app_backup.py
├── requirements.txt
├── .gitignore
│
├── src/
│   └── summarizer.py
│
└── data/
    ├── summaries.csv
    ├── test_articles.csv
    ├── evaluation_checklist.csv
    └── evaluation_results.csv
```

## ⚙️ Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/ipearlsuhani/AI-Powered-Text-Summarizer.git
```

2. Navigate to the project directory:

```bash
cd AI-Powered-Text-Summarizer
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the environment (Windows):

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
streamlit run app.py
```

## 🧪 Testing and Evaluation

The project was tested using 10 sample articles covering different topics, including:

- Artificial Intelligence
- Education Technology
- Healthcare
- Climate Change
- Cybersecurity
- Digital Banking
- Renewable Energy
- Social Media
- Space Technology
- Machine Learning

Generated summaries were reviewed using a human evaluation checklist based on:

- Key point coverage
- Factual consistency
- Unsupported claims
- Important omissions
- Overall summary quality

## ⚠️ Limitations

- Summary quality depends on the input text and pretrained model.
- Important details may sometimes be omitted.
- Generated summaries may contain unsupported information.
- Human review is recommended before relying on generated summaries.

## 🚀 Future Improvements

- Support for PDF and document uploads.
- Multilingual text summarization.
- Improved factual consistency checking.
- Additional summarization models.
- Automated summary quality evaluation.

## 👩‍💻 Developer

**Suhani Verma**

Bachelor of Computer Applications (BCA)  
Specialization: Artificial Intelligence

Invertis University, Bareilly

## 📜 Project Category

Academic Project | Artificial Intelligence | Natural Language Processing (NLP) | Text Summarization
