
from transformers import pipeline

# Pretrained AI summarization model
MODEL_NAME = "sshleifer/distilbart-cnn-6-6"

print("Loading AI summarization model...")

summarizer = pipeline(
    "summarization",
    model=MODEL_NAME,
    device=-1
)

print("AI model loaded successfully!")


# Function to summarize an article
def summarize_text(text):

    if not text.strip():
        return "Please enter some text."

    result = summarizer(
        text,
        max_length=130,
        min_length=30,
        do_sample=False,
        truncation=True
    )

    return result[0]["summary_text"]


# Test the summarization model
if __name__ == "__main__":

    article = """
    Artificial Intelligence is transforming the modern world.
    It is used in healthcare, education, banking and transportation.
    In healthcare, AI helps doctors analyze medical images and
    identify diseases. In education, AI provides personalized
    learning experiences to students. Businesses also use AI
    to automate repetitive tasks, improve productivity and
    make better decisions. However, responsible use of AI
    is important because it can create privacy and security risks.
    """

    print("\nORIGINAL ARTICLE:")
    print(article)

    print("\nGENERATED SUMMARY:")

    summary = summarize_text(article)

    print(summary)
