from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
import anthropic
from datetime import datetime, timedelta

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

app = Flask(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def get_news(query, days_back, num_articles):
    from_date = (datetime.now() - timedelta(days=int(days_back))).strftime("%Y-%m-%d")
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize={num_articles}&from={from_date}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles

def analyze_with_claude(query, articles):
    article_text = ""
    for i, article in enumerate(articles):
        date = article.get("publishedAt", "")[:10]
        source = article.get("source", {}).get("name", "Unknown")
        article_text += f"Article {i+1} [{date} | {source}]:\nTitle: {article['title']}\nSummary: {article['description']}\n\n"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""You are a senior market research analyst. The user has searched for "{query}".

IMPORTANT: Only reject the query if it is unambiguously a specific individual person — meaning it includes both a first and last name of a real private individual (e.g. "John Smith"). Do NOT reject company names that sound like names (e.g. "Phillips", "Johnson & Johnson", "Dell", "Dyson"). When in doubt, treat it as a company and proceed.

If it is clearly just a private individual with no company connection, respond with:
"This tool is designed for company and industry research only. Please enter a company name or industry."

Otherwise write a detailed research brief with these sections:

## Executive Summary
2-3 sentence overview of the current landscape.

## Key Trends
List and explain the most important trends. Be specific and cite article details.

## Major Players
Key companies, people, or organizations mentioned and their roles.

## Opportunities
What opportunities exist in this space right now?

## Risks & Challenges
What risks or headwinds should someone be aware of?

## Analyst Take
Your overall assessment — where is this headed in the next 6-12 months?

Be specific and analytical. Reference actual details from the articles.

Articles:
{article_text}"""
            }
        ]
    )
    return message.content[0].text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/research", methods=["POST"])
def research():
    data = request.get_json()
    query = data.get("query", "")
    days = data.get("days", 7)
    count = data.get("count", 10)

    articles = get_news(query, days, count)

    if not articles:
        return jsonify({"error": "No articles found. Try a broader search term or longer time range."})

    analysis = analyze_with_claude(query, articles)

    formatted_articles = []
    for a in articles:
        formatted_articles.append({
            "title": a.get("title", ""),
            "url": a.get("url", ""),
            "source": a.get("source", {}).get("name", "Unknown"),
            "date": a.get("publishedAt", "")[:10],
            "description": a.get("description", "")
        })

    return jsonify({
        "analysis": analysis,
        "articles": formatted_articles,
        "article_count": len(articles)
    })

if __name__ == "__main__":
app.run(host="0.0.0.0", port=5000, debug=False)