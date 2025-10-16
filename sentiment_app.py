import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

classifier = load_model()

st.title("Multilingual Sentiment Analyzer 😄🌏")
st.markdown("**Try Hindi, Hinglish or English sentences!**")

text = st.text_input("🔹 Enter your sentence:")

if st.button("Analyze") and text.strip():
    result = classifier(text)
    label = result[0]['label']
    score = result[0]['score']

    rating = int(label[0])  # Extract star number from "X stars"

    if rating <= 2:
        sentiment = "😞 Negative"
    elif rating == 3:
        sentiment = "😐 Neutral"
    else:
        sentiment = "😊 Positive"

    st.write("**Sentiment:**", sentiment)
    st.write("**Model Rating:**", label)
    st.write("**Confidence:**", round(score, 2))
