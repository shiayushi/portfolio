@echo off
cd "E:\NLP PROJECTS\AI Interview Bot"
set OPENAI_API_KEY=yourkey-if-any
streamlit run ai_interview_bot.py --server.headless false
pause
