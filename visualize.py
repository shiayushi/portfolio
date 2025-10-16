import csv
import matplotlib.pyplot as plt

def read_sentiment_scores(csv_file="answers.csv"):
    questions = []
    scores = []

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row['Question'])
            scores.append(float(row['Sentiment Score']))

    return questions, scores

def plot_sentiment_graph(questions, scores):
    plt.figure(figsize=(10, 5))
    colors = ['green' if s > 0.1 else 'red' if s < -0.1 else 'gray' for s in scores]

    plt.bar(range(len(scores)), scores, color=colors)
    plt.xticks(range(len(scores)), [f"Q{i+1}" for i in range(len(scores))], rotation=45)
    plt.ylabel("Sentiment Score")
    plt.title("Sentiment Analysis of Interview Answers")
    plt.grid(axis='y')
    plt.ylim(-1, 1)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    q, s = read_sentiment_scores()
    plot_sentiment_graph(q, s)
