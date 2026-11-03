import io
from datetime import datetime

import pandas as pd
import streamlit as st
from supabase import create_client
from src.summarizer import summarize_text

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Summarize AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #f4f7fc; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1250px; }
.hero {
    background: linear-gradient(120deg, #101c36, #244c83);
    padding: 35px; border-radius: 18px; color: white; margin-bottom: 25px;
}
.hero h1 { color: white; font-size: 38px; margin-bottom: 10px; }
.hero p { color: #d4e3fa; font-size: 16px; }
.section-card {
    background: white; padding: 22px; border-radius: 15px;
    border: 1px solid #e2e8f0; min-height: 180px;
}
.stButton > button {
    background-color: #2458a6; color: white; border-radius: 9px;
    border: none; font-weight: 600; min-height: 43px;
}
.stButton > button:hover { background-color: #173e78; color: white; }
.footer { text-align: center; color: #718096; padding: 25px; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

MODEL_NAME = "sshleifer/distilbart-cnn-6-6"

# ---------------- SESSION STATE ----------------
defaults = {
    "article_input": "",
    "summary": "",
    "original_article": "",
    "access_token": None,
    "refresh_token": None,
    "user_id": None,
    "user_email": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- SUPABASE CONNECTION ----------------
def get_supabase_client():
    """Create a client for this Streamlit session and restore its user session."""
    try:
        url = st.secrets.get("SUPABASE_URL", "")
        key = st.secrets.get("SUPABASE_KEY", "")
    except Exception:
        return None

    if not url or not key:
        return None

    try:
        client = create_client(url, key)
        access_token = st.session_state.get("access_token")
        refresh_token = st.session_state.get("refresh_token")
        if access_token and refresh_token:
            client.auth.set_session(access_token, refresh_token)
        return client
    except Exception as exc:
        st.error(f"Could not connect to Supabase: {exc}")
        return None


supabase = get_supabase_client()


def current_user_id():
    return st.session_state.get("user_id")


def clear_login():
    for key in ("access_token", "refresh_token", "user_id", "user_email"):
        st.session_state[key] = None


def download_summary_buttons(summary_text):
    if not summary_text:
        return
    st.download_button(
        "⬇️ Download Summary as TXT",
        data=summary_text.encode("utf-8"),
        file_name="AI_Generated_Summary.txt",
        mime="text/plain",
        key="download_summary_txt",
    )
    # PDF download is optional; the app continues to work if ReportLab is absent.
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 50
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(45, y, "AI Generated Summary")
        y -= 30
        pdf.setFont("Helvetica", 10)
        for paragraph in summary_text.splitlines() or [""]:
            words = paragraph.split()
            line = ""
            for word in words:
                candidate = f"{line} {word}".strip()
                if pdf.stringWidth(candidate, "Helvetica", 10) > width - 90:
                    pdf.drawString(45, y, line)
                    y -= 15
                    line = word
                    if y < 55:
                        pdf.showPage()
                        pdf.setFont("Helvetica", 10)
                        y = height - 50
                else:
                    line = candidate
            pdf.drawString(45, y, line)
            y -= 18
            if y < 55:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50
        pdf.save()
        st.download_button(
            "⬇️ Download Summary as PDF",
            data=buffer.getvalue(),
            file_name="AI_Generated_Summary.pdf",
            mime="application/pdf",
            key="download_summary_pdf",
        )
    except ImportError:
        st.caption("PDF export is unavailable until the `reportlab` package is added.")

# ---------------- DOCUMENT TEXT EXTRACTION ----------------
def extract_uploaded_text(uploaded_file):
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()

    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF support requires the pypdf package.") from exc
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("DOCX support requires the python-docx package.") from exc
        document = Document(io.BytesIO(raw))
        return "\n".join(p.text for p in document.paragraphs)
    if name.endswith(".pptx"):
        try:
            from pptx import Presentation
        except ImportError as exc:
            raise RuntimeError("PPTX support requires the python-pptx package.") from exc
        presentation = Presentation(io.BytesIO(raw))
        lines = []
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    lines.append(shape.text.strip())
        return "\n".join(lines)
    raise ValueError("Unsupported file type. Upload PDF, DOCX, PPTX, or TXT.")


# ---------------- SIDEBAR / AUTHENTICATION ----------------
with st.sidebar:
    st.title("🧠 Summarize AI")
    st.caption("Intelligent NLP Workspace")
    st.divider()

    st.subheader("Account")
    if current_user_id():
        st.success(f"Logged in: {st.session_state.get('user_email', 'User')}")
        if st.button("Log out", use_container_width=True):
            clear_login()
            st.rerun()
    else:
        auth_tab = st.radio("Choose account action", ["Login", "Sign Up"], horizontal=True)
        with st.form("authentication_form"):
            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")
            auth_submit = st.form_submit_button(auth_tab, use_container_width=True)

        if auth_submit:
            if not supabase:
                st.error("Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY in Streamlit Secrets.")
            elif not email.strip() or not password:
                st.warning("Enter both email and password.")
            else:
                try:
                    if auth_tab == "Sign Up":
                        response = supabase.auth.sign_up({"email": email.strip(), "password": password})
                        session = getattr(response, "session", None)
                        user = getattr(response, "user", None)
                        if session:
                            st.session_state.access_token = session.access_token
                            st.session_state.refresh_token = session.refresh_token
                            st.session_state.user_id = user.id if user else None
                            st.session_state.user_email = email.strip()
                            st.success("Account created and logged in.")
                        else:
                            st.success("Account created. Check your email and confirm your address, then log in.")
                    else:
                        response = supabase.auth.sign_in_with_password(
                            {"email": email.strip(), "password": password}
                        )
                        session = response.session
                        user = response.user
                        st.session_state.access_token = session.access_token
                        st.session_state.refresh_token = session.refresh_token
                        st.session_state.user_id = user.id
                        st.session_state.user_email = email.strip()
                        st.success("Login successful.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Authentication failed: {exc}")

    st.divider()
    page = st.radio("Navigation", ["Home", "History", "Evaluation", "About Project"])
    st.divider()
    st.subheader("Model Information")
    st.success("Model ready when first used")
    st.write("**Model:**")
    st.caption("DistilBART CNN 6-6")
    st.write("**Framework:**")
    st.caption("Hugging Face Transformers")
    st.write("**Processing:**")
    st.caption("CPU")
    st.divider()
    st.caption("AI-Powered Text Summarizer | Version 2.0")

# ---------------- HOME PAGE ----------------
if page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>Turn long reads into clear insights.</h1>
        <p>Generate meaningful and concise summaries from lengthy articles using Artificial Intelligence.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Article Workspace")
    st.write("Paste text or upload a document. Supported formats: PDF, DOCX, PPTX and TXT.")

    uploaded_file = st.file_uploader(
        "Upload an article/document",
        type=["pdf", "docx", "pptx", "txt"],
        key="article_upload",
    )
    if uploaded_file is not None:
        if st.button("Extract text from uploaded file"):
            try:
                extracted = extract_uploaded_text(uploaded_file)
                if extracted.strip():
                    st.session_state.article_input = extracted
                    st.success("Text extracted. Review it below, then generate a summary.")
                    st.rerun()
                else:
                    st.warning("No selectable text was found. Scanned PDFs requiring OCR are not supported.")
            except Exception as exc:
                st.error(f"Could not read the uploaded file: {exc}")

    if st.button("Clear Article", key="clear_article"):
        st.session_state.article_input = ""
        st.session_state.summary = ""
        st.session_state.original_article = ""
        st.rerun()

    article = st.text_area(
        "Your original article",
        key="article_input",
        height=230,
        placeholder="Paste your article here or extract it from an uploaded document...",
    )
    original_words = len(article.split())
    st.caption(f"Original word count: {original_words}")

    if st.button("✨ Generate AI Summary", use_container_width=True):
        if not article.strip():
            st.warning("Please enter an article first.")
        elif original_words < 30:
            st.warning("Please enter at least 30 words.")
        else:
            with st.spinner("AI is analyzing your article..."):
                try:
                    generated_summary = summarize_text(article)
                    st.session_state.summary = generated_summary
                    st.session_state.original_article = article

                    if current_user_id() and supabase:
                        record = {
                            "user_id": current_user_id(),
                            "original_text": article,
                            "generated_summary": generated_summary,
                        }
                        supabase.table("summaries").insert(record).execute()
                        st.success("Summary generated and saved to your private account history.")
                    else:
                        st.success("Summary generated. Log in to save it to your private history.")
                except Exception as exc:
                    st.error(f"Error generating or saving the summary: {exc}")

    if st.session_state.summary:
        st.divider()
        st.subheader("Summary Results")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📄 Original Article")
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.write(st.session_state.original_article)
            st.markdown("</div>", unsafe_allow_html=True)
            st.caption(f"Original words: {len(st.session_state.original_article.split())}")
        with col2:
            st.markdown("### ✨ AI Generated Summary")
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.write(st.session_state.summary)
            st.markdown("</div>", unsafe_allow_html=True)
            st.caption(f"Summary words: {len(st.session_state.summary.split())}")

        original_count = len(st.session_state.original_article.split())
        summary_count = len(st.session_state.summary.split())
        compression = (1 - summary_count / original_count) * 100 if original_count else 0
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Original Words", original_count)
        m2.metric("Summary Words", summary_count)
        m3.metric("Text Reduction", f"{compression:.1f}%")
        download_summary_buttons(st.session_state.summary)

# ---------------- HISTORY PAGE ----------------
elif page == "History":
    st.title("📚 My Summary History")
    st.write("Your saved summaries are private and visible only to your account.")
    if not current_user_id() or not supabase:
        st.warning("Please log in to access your private summary history.")
    else:
        try:
            response = (
                supabase.table("summaries").select("*")
                .eq("user_id", current_user_id())
                .order("created_at", desc=True).execute()
            )
            history = response.data or []
            if history:
                st.metric("Total Saved Summaries", len(history))
                for index, chosen in enumerate(history):
                    created = str(chosen.get("created_at", ""))
                    with st.expander(f"{created[:19]} | {str(chosen.get('original_text', ''))[:75]}"):
                        left, right = st.columns(2)
                        with left:
                            st.markdown("**Original Article**")
                            st.write(chosen.get("original_text", ""))
                        with right:
                            st.markdown("**Generated Summary**")
                            st.write(chosen.get("generated_summary", ""))
                        download_summary_buttons(chosen.get("generated_summary", ""))
                history_df = pd.DataFrame(history)
                st.download_button(
                    "Download My Summary History CSV",
                    data=history_df.to_csv(index=False).encode("utf-8"),
                    file_name="my_summary_history.csv",
                    mime="text/csv",
                )
            else:
                st.info("You have not saved any summaries yet.")
        except Exception as exc:
            st.error(f"Could not load your history: {exc}")

# ---------------- EVALUATION PAGE ----------------
elif page == "Evaluation":
    st.title("🧪 Summary Quality Evaluation")
    st.write(
        "Review an AI-generated summary against its original article. "
        "This is a human-review checklist, not an automatic accuracy score."
    )
    if not current_user_id() or not supabase:
        st.warning("Please log in to access your private evaluations.")
    else:
        try:
            result = (
                supabase.table("summaries").select("*")
                .eq("user_id", current_user_id())
                .order("created_at", desc=True).execute()
            )
            summaries = result.data or []
            if not summaries:
                st.info("Generate and save a summary first.")
            else:
                labels = {
                    row["id"]: (
                        f'{str(row.get("created_at", ""))[:19]} | '
                        f'{str(row.get("original_text", ""))[:75]}'
                    )
                    for row in summaries
                }
                selected_id = st.selectbox(
                    "Choose a summary to evaluate",
                    list(labels),
                    format_func=lambda value: labels[value],
                )
                selected = next(row for row in summaries if row["id"] == selected_id)
                left, right = st.columns(2)
                with left:
                    st.markdown("### 📄 Original Article")
                    st.write(selected.get("original_text", ""))
                with right:
                    st.markdown("### ✨ Generated Summary")
                    st.write(selected.get("generated_summary", ""))

                st.divider()
                st.subheader("Human Review Checklist")
                st.caption("Use 1 = Poor and 5 = Excellent.")
                with st.form("summary_evaluation_form"):
                    coverage = st.slider(
                        "1. How well does the summary cover the key points?", 1, 5, 3
                    )
                    consistency = st.slider(
                        "2. How factually consistent is the summary?", 1, 5, 3
                    )
                    unsupported = st.text_area(
                        "3. Unsupported claims (write 'None found' if none)"
                    )
                    omissions = st.text_area(
                        "4. Important omissions (write 'None found' if none)"
                    )
                    comments = st.text_area("5. Reviewer notes")
                    submitted = st.form_submit_button(
                        "Save Evaluation", use_container_width=True
                    )

                if submitted:
                    evaluation = {
                        "summary_id": selected_id,
                        "user_id": current_user_id(),
                        "key_point_coverage": str(coverage),
                        "unsupported_claims": unsupported.strip() or "None found",
                        "important_omissions": omissions.strip() or "None found",
                        "factual_consistency": str(consistency),
                        "comments": comments.strip() or "None",
                    }
                    supabase.table("evaluations").insert(evaluation).execute()
                    st.success("Your evaluation has been saved privately.")

                st.divider()
                st.subheader("My Saved Evaluations")
                reviews_response = (
                    supabase.table("evaluations").select("*")
                    .eq("user_id", current_user_id())
                    .order("created_at", desc=True).execute()
                )
                reviews = reviews_response.data or []
                if reviews:
                    review_df = pd.DataFrame(reviews)
                    st.dataframe(review_df, use_container_width=True, hide_index=True)
                    st.download_button(
                        "Download My Evaluation Results CSV",
                        data=review_df.to_csv(index=False).encode("utf-8"),
                        file_name="my_evaluation_results.csv",
                        mime="text/csv",
                    )
                else:
                    st.info("No evaluations saved yet.")
        except Exception as exc:
            st.error(f"Could not load or save evaluations: {exc}")

# ---------------- ABOUT PAGE ----------------
elif page == "About Project":
    st.title("About This Project")
    st.write("""
    **AI-Powered Text Summarizer** is an NLP-based application designed to convert lengthy articles into concise summaries.

    ### Technologies Used
    - Python
    - Hugging Face Transformers
    - DistilBART pretrained model
    - Streamlit
    - Supabase Authentication and PostgreSQL database
    - Pandas

    ### Project Features
    - Public text summarization without login
    - Email/password signup and login
    - Private, user-specific summary history and evaluations
    - PDF, DOCX, PPTX, and TXT text extraction
    - TXT, PDF, and CSV downloads

    ### Responsible AI
    Generated summaries may omit context or contain unsupported information. Always compare the summary against the original article. Scanned PDFs requiring OCR are not supported in this version.
    """)
    st.info(
        "This application is an academic NLP project. "
        "AI-generated content should be reviewed by humans."
    )

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    AI-Powered Text Summarizer | Built with Python and Streamlit<br>
    Responsible AI • Human Review • NLP
</div>
""", unsafe_allow_html=True)
