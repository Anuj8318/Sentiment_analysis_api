from flask import Flask, request, jsonify
import pandas as pd
import io

import requests

from config import GROQ_API_KEY

app = Flask(__name__)
# file = "customer_reviews.xlsx"
def read_file(file):
    if file.filename.endswith('.xlsx'):
        return pd.read_excel(file)
    elif file.filename.endswith('.csv'):
        return pd.read_csv(file)
    else:
        raise ValueError("Unsupported file format. Please upload an XLSX or CSV file.")

def analyze_sentiment_groq(review):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a sentiment analysis expert. Analyze the sentiment of the following review and respond with a single word: POSITIVE, NEGATIVE, or NEUTRAL."
            },
            {
                "role": "user",
                "content": review
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        sentiment = response.json()['choices'][0]['message']['content'].strip().upper()
        return sentiment
    else:
        raise Exception(f"Groq API error: {response.text}")

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        df = read_file(file)
        reviews = df['Review'].tolist()
        sentiments = [analyze_sentiment_groq(review) for review in reviews]
        
        sentiment_counts = {
            "positive": sentiments.count("POSITIVE"),
            "negative": sentiments.count("NEGATIVE"),
            "neutral": sentiments.count("NEUTRAL")
        }
        total = sum(sentiment_counts.values())
        sentiment_scores = {
            "positive": sentiment_counts["positive"] / total,
            "negative": sentiment_counts["negative"] / total,
            "neutral": sentiment_counts["neutral"] / total
        }
        
        return jsonify(sentiment_scores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
