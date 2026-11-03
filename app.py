                download_summary_buttons(chosen.get("generated_summary", ""))
            else:
                st.info("You have not saved any summaries yet.")
        except Exception as exc:
            st.error(f"Could not load your history: {exc}")

# ---------------- EVALUATION PAGE ----------------
elif page == "Evaluation":
    st.title("🧪 Summary Quality Evaluation")
    st.write("Review an AI-generated summary against its original article. This is a human-review checklist, not an automatic accuracy score.")
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
                    row["id"]: f'{str(row.get("created_at", ""))[:19]} | {str(row.get("original_text", ""))[:75]}'
                    for row in summaries
                }
                selected_id = st.selectbox("Choose a summary to evaluate", list(labels), format_func=lambda x: labels[x])
                selected = next(row for row in summaries if row["id"] == selected_id)
                left, right = st.columns(2)
                with left:
                    st.markdown("### 📄 Original Article")
                    st.write(selected["original_text"])
                with right:
                    st.markdown("### ✨ Generated Summary")
                    st.write(selected["generated_summary"])

                st.divider()
                st.subheader("Human Review Checklist")
                st.caption("Use 1 = Poor and 5 = Excellent.")
                with st.form("summary_evaluation_form"):
                    coverage = st.slider("1. How well does the summary cover the key points?", 1, 5, 3)
                    consistency = st.slider("2. How factually consistent is the summary?", 1, 5, 3)
                    unsupported = st.text_area("3. Unsupported claims (write 'None found' if none)")
                    omissions = st.text_area("4. Important omissions (write 'None found' if none)")
                    comments = st.text_area("5. Reviewer notes")
                    submitted = st.form_submit_button("Save Evaluation", use_container_width=True)

                if submitted:
                    evaluation = {
                        "summary_id": selected_id,
                        "user_id": current_user_id(),
                        "key_point_coverage": str(coverage),
                        "unsupported_claims": unsupported.strip() or "None found",
                        "important_omissions": omissions.strip() or "None found",
                        "factual_consistency": str(consistency),
                        "comments": comments.strip() or "None"
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
                        file_name="my_evaluation_results.csv", mime="text/csv"
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
    st.info("This application is an academic NLP project. AI-generated content should be reviewed by humans.")

st.markdown("""
<div class="footer">
AI-Powered Text Summarizer | Built with Python and Streamlit<br>
Responsible AI • Human Review • NLP
</div>
""", unsafe_allow_html=True)
