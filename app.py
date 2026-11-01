
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from src.summarizer import summarize_text

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Summarize AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

.hero {
    background: linear-gradient(120deg, #101c36, #244c83);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 38px;
    margin-bottom: 10px;
}

.hero p {
    color: #d4e3fa;
    font-size: 16px;
}

.section-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #e2e8f0;
    min-height: 180px;
}

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.stButton > button {
    background-color: #2458a6;
    color: white;
    border-radius: 9px;
    border: none;
    font-weight: 600;
    min-height: 43px;
}

.stButton > button:hover {
    background-color: #173e78;
    color: white;
}

.footer {
    text-align: center;
    color: #718096;
    padding: 25px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- DATA STORAGE ----------------

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

CSV_FILE = DATA_DIR / "summaries.csv"
EVALUATION_FILE = DATA_DIR / "evaluation_results.csv"


# ---------------- SESSION STATE ----------------

if "article_input" not in st.session_state:
    st.session_state.article_input = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "original_article" not in st.session_state:
    st.session_state.original_article = ""


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 Summarize AI")
    st.caption("Intelligent NLP Workspace")

    st.divider()

    page = st.radio(
        "Navigation",
        ["Home", "History", "Evaluation", "About Project"]
    )

    st.divider()

    st.subheader("Model Information")

    st.success("Model loaded")

    st.write("**Model:**")
    st.caption("DistilBART CNN 6-6")

    st.write("**Framework:**")
    st.caption("Hugging Face Transformers")

    st.write("**Processing:**")
    st.caption("CPU")

    st.divider()

    st.caption("AI-Powered Text Summarizer | Version 1.0")


# ---------------- HOME PAGE ----------------

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Turn long reads into clear insights.</h1>
        <p>
        Generate meaningful and concise summaries from lengthy
        articles using Artificial Intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Article Workspace")

    st.write(
        "Paste your article below and let AI extract its key information."
    )

    if st.button("Clear Article", key="clear_article"):
        st.session_state.article_input = ""
        st.session_state.summary = ""
        st.session_state.original_article = ""
        st.rerun()

    article = st.text_area(
        "Your original article",
        key="article_input",
        height=230,
        placeholder="Paste your article here..."
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

                    new_record = pd.DataFrame([{
                        "date": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "model": "sshleifer/distilbart-cnn-6-6",
                        "original_article": article,
                        "generated_summary": generated_summary
                    }])

                    if CSV_FILE.exists():

                        old_records = pd.read_csv(CSV_FILE)

                        records = pd.concat(
                            [old_records, new_record],
                            ignore_index=True
                        )

                    else:

                        records = new_record

                    records.to_csv(CSV_FILE, index=False)

                    st.success("Summary generated and saved successfully!")

                except Exception as error:

                    st.error(f"Error generating summary: {error}")


    # DISPLAY RESULTS

    if st.session_state.summary:

        st.divider()

        st.subheader("Summary Results")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 📄 Original Article")

            st.markdown(
                '<div class="section-card">',
                unsafe_allow_html=True
            )

            st.write(st.session_state.original_article)

            st.markdown("</div>", unsafe_allow_html=True)

            st.caption(
                f"Original words: "
                f"{len(st.session_state.original_article.split())}"
            )

        with col2:

            st.markdown("### ✨ AI Generated Summary")

            st.markdown(
                '<div class="section-card">',
                unsafe_allow_html=True
            )

            st.write(st.session_state.summary)

            st.markdown("</div>", unsafe_allow_html=True)

            st.caption(
                f"Summary words: "
                f"{len(st.session_state.summary.split())}"
            )

        original_count = len(
            st.session_state.original_article.split()
        )

        summary_count = len(
            st.session_state.summary.split()
        )

        compression = (
            (1 - summary_count / original_count) * 100
            if original_count > 0 else 0
        )

        st.divider()

        m1, m2, m3 = st.columns(3)

        m1.metric("Original Words", original_count)

        m2.metric("Summary Words", summary_count)

        m3.metric(
            "Text Reduction",
            f"{compression:.1f}%"
        )

        st.download_button(
            "⬇️ Download Summary",
            data=st.session_state.summary,
            file_name="AI_Generated_Summary.txt",
            mime="text/plain"
        )


# ---------------- HISTORY PAGE ----------------

elif page == "History":

    st.title("📚 Summary History")

    st.write("Review previously generated summaries.")

    if CSV_FILE.exists():

        history = pd.read_csv(CSV_FILE)

        st.metric("Total Summaries", len(history))

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        csv_data = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download History CSV",
            data=csv_data,
            file_name="summary_history.csv",
            mime="text/csv"
        )

    else:

        st.info("No summaries have been generated yet.")


# ---------------- EVALUATION PAGE ----------------

elif page == "Evaluation":

    st.title("🧪 Summary Quality Evaluation")
    st.write(
        "Review an AI-generated summary against its original article. "
        "This is a human-review checklist, not an automatic accuracy score."
    )

    if CSV_FILE.exists():
        history = pd.read_csv(CSV_FILE)

        if not history.empty:
            history["review_label"] = (
                history["date"].astype(str) + " | "
                + history["original_article"].astype(str).str.slice(0, 75)
            )
            selected_index = st.selectbox(
                "Choose a summary to evaluate",
                options=list(history.index),
                format_func=lambda i: history.loc[i, "review_label"]
            )
            selected = history.loc[selected_index]

            original_text = str(selected["original_article"])
            summary_text = str(selected["generated_summary"])

            left, right = st.columns(2)
            with left:
                st.markdown("### 📄 Original Article")
                st.write(original_text)
            with right:
                st.markdown("### ✨ Generated Summary")
                st.write(summary_text)

            st.divider()
            st.subheader("Human Review Checklist")
            st.caption("Use 1 = Poor and 5 = Excellent for the rating questions.")

            with st.form("summary_evaluation_form"):
                coverage = st.slider(
                    "1. How well does the summary cover the key points?",
                    min_value=1, max_value=5, value=3
                )
                consistency = st.slider(
                    "2. How factually consistent is the summary with the article?",
                    min_value=1, max_value=5, value=3
                )
                unsupported = st.text_area(
                    "3. Unsupported claims (write 'None found' if there are none)",
                    placeholder="Mention any statement that is not supported by the article..."
                )
                omissions = st.text_area(
                    "4. Important omissions (write 'None found' if there are none)",
                    placeholder="Mention important details missing from the summary..."
                )
                notes = st.text_area(
                    "5. Reviewer notes",
                    placeholder="Add any other observations..."
                )
                submitted = st.form_submit_button(
                    "Save Evaluation", use_container_width=True
                )

            if submitted:
                evaluation_record = pd.DataFrame([{
                    "review_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "summary_date": str(selected["date"]),
                    "model": str(selected.get("model", "Unknown")),
                    "coverage_rating_1_to_5": coverage,
                    "factual_consistency_rating_1_to_5": consistency,
                    "unsupported_claims": unsupported.strip() or "Not recorded",
                    "important_omissions": omissions.strip() or "Not recorded",
                    "reviewer_notes": notes.strip() or "None"
                }])

                if EVALUATION_FILE.exists():
                    previous = pd.read_csv(EVALUATION_FILE)
                    evaluation_record = pd.concat(
                        [previous, evaluation_record], ignore_index=True
                    )

                evaluation_record.to_csv(EVALUATION_FILE, index=False)
                st.success("Evaluation saved successfully!")
                st.info("The ratings are human assessments and should not be treated as an automated model accuracy score.")

            if EVALUATION_FILE.exists():
                st.divider()
                st.subheader("Saved Evaluation Records")
                saved_reviews = pd.read_csv(EVALUATION_FILE)
                st.dataframe(saved_reviews, use_container_width=True, hide_index=True)
                st.download_button(
                    "Download Evaluation Results",
                    data=saved_reviews.to_csv(index=False).encode("utf-8"),
                    file_name="evaluation_results.csv",
                    mime="text/csv"
                )
        else:
            st.info("Generate at least one summary on the Home page before evaluating it.")
    else:
        st.info("Generate at least one summary on the Home page before evaluating it.")


# ---------------- ABOUT PAGE ----------------

elif page == "About Project":

    st.title("About This Project")

    st.write("""
    **AI-Powered Text Summarizer** is an NLP-based application
    designed to convert lengthy articles into concise summaries.

    ### Technologies Used

    - Python
    - Hugging Face Transformers
    - DistilBART pretrained model
    - Streamlit
    - Pandas

    ### Project Objectives

    - Reduce the time needed to read lengthy articles.
    - Extract important information from source text.
    - Preserve original articles and generated summaries.
    - Support human review of AI-generated content.

    ### Responsible AI

    Generated summaries may omit important context or
    contain unsupported information. Always compare
    the summary against the original article.
    """)

    st.info(
        "This application is an academic NLP project. "
        "AI-generated content should be reviewed by humans."
    )


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    AI-Powered Text Summarizer | Built with Python and Streamlit
    <br>
    Responsible AI • Human Review • NLP
</div>
""", unsafe_allow_html=True)
