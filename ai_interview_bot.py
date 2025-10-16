import streamlit as st
import pandas as pd
import os
import csv
from textblob import TextBlob

# Load questions from .txt file or use default ones
def load_questions(filename="questions.txt"):
    if not os.path.exists(filename):
        return [
            "Tell me about yourself.",
            "What are your strengths?",
            "Why should we hire you?",
            "Describe a challenge you overcame.",
            "Where do you see yourself in 5 years?"
        ]
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Analyze the answer
def analyze_answer(answer):
    feedback = []
    words = answer.split()
    long_words = [w for w in words if len(w) > 6]

    if len(words) < 10:
        feedback.append("Try to give a longer answer with more detail.")
    else:
        feedback.append("Nice length. You explained well.")

    if not answer.strip().endswith('.'):
        feedback.append("Consider ending with proper punctuation.")

    if len(long_words) < 3:
        feedback.append("Try using more descriptive vocabulary.")

    blob = TextBlob(answer)
    polarity = round(blob.sentiment.polarity, 2)
    sentiment_type = (
        "Positive 😊" if polarity > 0.1 else
        "Negative 😕" if polarity < -0.1 else
        "Neutral 😐"
    )

    return feedback, polarity, sentiment_type

# Save responses to CSV
def save_to_csv(question, answer, feedback, polarity, sentiment_type, filename="answers.csv"):
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Question', 'Answer', 'Feedback', 'Sentiment Score', 'Sentiment Type'])
        writer.writerow([question, answer, "; ".join(feedback), polarity, sentiment_type])

# Streamlit App
def main():
    st.set_page_config(page_title="AI Interview Bot", page_icon="🤖")
    st.title("🤖 AI Interview Bot (Offline + Sentiment)")
    st.markdown("Practice answering interview questions and get real-time feedback and sentiment analysis.")

    questions = load_questions()
    selected_question = st.selectbox("📌 Select a Question", questions)

    answer = st.text_area("📝 Your Answer", height=150)

    if st.button("✨ Analyze Answer"):
        if answer.strip() == "":
            st.warning("Please enter your answer.")
        else:
            feedback, polarity, sentiment_type = analyze_answer(answer)

            st.markdown("### ✅ Feedback")
            for fb in feedback:
                st.write(f"🔹 {fb}")

            st.markdown("### 💬 Sentiment Analysis")
            st.info(f"**Score:** `{polarity}` → {sentiment_type}")

            save_to_csv(selected_question, answer, feedback, polarity, sentiment_type)
            st.success("✅ Response saved to CSV!")

if __name__ == "__main__":
    main()
