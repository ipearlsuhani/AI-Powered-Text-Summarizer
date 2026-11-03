# AI-Powered Text Summarizer

An NLP-based web application that converts lengthy articles into concise, readable summaries using a pretrained DistilBART model. Built with Python and Streamlit, the application also supports document text extraction, user authentication, private summary history, and human-led summary quality evaluation.

## 🚀 Live Application

**Streamlit App:** https://ai-powered-text-summarizer-767.streamlit.app/

**GitHub Repository:** https://github.com/ipearlsuhani/AI-Powered-Text-Summarizer

---

## 📌 Project Overview

Reading lengthy articles, reports, and documents can be time-consuming. This project uses a pretrained Natural Language Processing (NLP) model to generate shorter versions of input text while retaining important information.

Users can paste text or upload supported documents, generate AI-powered summaries, download the results, and save their summaries to a private account. The application also provides a human-review checklist to evaluate the quality of generated summaries.

## ✨ Key Features

- **AI Text Summarization:** Generates concise summaries from lengthy articles.
- **Document Upload:** Extracts text from PDF, DOCX, PPTX, and TXT files.
- **User Authentication:** Supports email/password signup and login.
- **Private Summary History:** Stores summaries associated with individual user accounts.
- **Summary Quality Evaluation:** Provides a human-review checklist to assess summary quality.
- **Download Options:** Download summaries in TXT and PDF formats.
- **CSV Export:** Export personal summary history and evaluation records.
- **Interactive Interface:** Simple and user-friendly Streamlit application.

> Note: Scanned PDFs that require OCR are not supported in the current version. Uploaded documents must contain selectable text.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Hugging Face Transformers | NLP model integration |
| DistilBART | Pretrained text summarization model |
| PyTorch | Deep learning framework |
| Pandas | Data handling and CSV export |
| Supabase | Authentication and PostgreSQL database |
| pypdf | PDF text extraction |
| python-docx | DOCX text extraction |
| python-pptx | PPTX text extraction |
| ReportLab | PDF generation |
| Git and GitHub | Version control and source-code management |
| Streamlit Community Cloud | Application deployment |

## 🤖 AI Model Used

**Model:** `sshleifer/distilbart-cnn-6-6`

The application uses a pretrained DistilBART model available through Hugging Face Transformers.

The model is designed for abstractive text summarization. It processes the input article and generates a shorter version containing its important information.

**Processing Configuration:**
- Model: DistilBART CNN 6-6
- Framework: Hugging Face Transformers
- Deep Learning Library: PyTorch
- Processing Device: CPU
- Model Training: Existing pretrained model (no additional training in this project)

The current application runs model inference on the CPU. GPU processing is not enabled.

## 🔄 Application Workflow

1. Open the web application.
2. Paste an article or upload a supported document.
3. Extract the text if a document is uploaded.
4. Review the original article.
5. Click **Generate AI Summary**.
6. View the original article and generated summary.
7. Download the summary in the available formats.
8. Sign up or log in to save summaries privately.
9. Visit the History section to access saved summaries.
10. Use the Evaluation section to review summary quality.

## 📂 Project Structure

```text
AI-Powered-Text-Summarizer/
│
├── app.py
├── src/
│   └── summarizer.py
│
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   └── secrets.toml
│
└── README.md
```

**File Description:**

- `app.py` – Main Streamlit application containing the interface, authentication, document upload, history, and evaluation features.
- `src/summarizer.py` – Loads the pretrained DistilBART model and generates summaries.
- `requirements.txt` – Contains the Python dependencies required by the project.
- `.gitignore` – Specifies files that should not be uploaded to GitHub.
- `.streamlit/secrets.toml` – Stores local application credentials and configuration. This file must remain private.
- `README.md` – Project documentation.

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ipearlsuhani/AI-Powered-Text-Summarizer.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Powered-Text-Summarizer
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Supabase

Create a `.streamlit/secrets.toml` file and add your own Supabase credentials:

```toml
SUPABASE_URL = "YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY = "YOUR_SUPABASE_PUBLISHABLE_KEY"
```

Make sure this file is included in `.gitignore`. Never upload private credentials or secret keys to GitHub.

The Supabase project should have the required `summaries` and `evaluations` tables, authentication enabled, and appropriate Row Level Security (RLS) policies.

For Streamlit Community Cloud, configure the same credentials in the application's Secrets settings.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open locally, usually at:

`http://localhost:8501`

## 🗄️ Database and Authentication

The application uses Supabase for authentication and persistent data storage.

- Email/password authentication allows users to create accounts and log in.
- Summary records are associated with the authenticated user's ID.
- Evaluation records are linked to the corresponding summary and user.
- Users can access their own saved summaries and evaluations.
- Row Level Security (RLS) policies help protect user-specific records.

Users can generate summaries without logging in. However, saving summaries to private history and accessing saved evaluations requires authentication.

## 🧪 Summary Quality Evaluation

The Evaluation section provides a human-review checklist to assess generated summaries.

It includes:

1. **Key-Point Coverage:** Checks whether important information from the original article is included.
2. **Factual Consistency:** Reviews whether the generated summary is consistent with the original content.
3. **Unsupported Claims:** Identifies statements that are not supported by the source article.
4. **Important Omissions:** Records important information missing from the summary.
5. **Reviewer Comments:** Allows additional observations and feedback.

The evaluation is a human assessment, not an automated factuality score.

## ⚠️ Limitations

- The current model runs on CPU, which may take longer than GPU processing.
- Scanned PDFs requiring OCR are not supported.
- Summary quality depends on the original input and pretrained model.
- Very long inputs may be subject to model input-length and processing limitations.
- Generated summaries should be reviewed before being used as factual information.

## 🔮 Future Enhancements

- OCR support for scanned documents.
- GPU-based model inference.
- Support for additional languages.
- Integration of more pretrained summarization models.
- Advanced automated summary evaluation.
- Additional document formats and improved processing performance.

## 👩‍💻 Author

**Suhani Verma**

Bachelor of Computer Applications (BCA) – Artificial Intelligence  
Invertis University, Bareilly

---

*Developed as an academic project to explore Natural Language Processing, pretrained language models, and practical AI application development.*
