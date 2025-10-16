import streamlit as st
from textblob import TextBlob
import csv
import os

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

def save_to_csv(question, answer, feedback, polarity, sentiment_type, filename="answers.csv"):
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Question', 'Answer', 'Feedback', 'Sentiment Score', 'Sentiment Type'])
        writer.writerow([question, answer, "; ".join(feedback), polarity, sentiment_type])

st.set_page_config(page_title="AI Interview Bot", layout="centered")
st.title("🧠 AI Interview Bot (Offline + Sentiment)")

questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "Why should we hire you?",
    "Describe a challenge you overcame.",
    "Where do you see yourself in 5 years?"
]

selected_q = st.selectbox("Select a Question:", questions)
user_answer = st.text_area("📝 Your Answer:", height=150)

if st.button("Analyze"):
    if user_answer.strip() == "":
        st.warning("Please write an answer.")
    else:
        fb, score, senti = analyze_answer(user_answer)
        st.subheader("✅ Feedback:")
        for f in fb:
            st.markdown(f"- {f}")
        st.subheader("💬 Sentiment Score:")
        st.write(f"**{score} → {senti}**")

        save_to_csv(selected_q, user_answer, fb, score, senti)
        st.success("Saved to answers.csv ✅")
