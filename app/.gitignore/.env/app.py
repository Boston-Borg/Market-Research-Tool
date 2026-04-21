import streamlit as st
import requests
import os
from dotenv import load_dotenv
import anthropic

# Load API keys from .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Set up the Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def get_news(query):
    """Fetch news articles for a given query"""
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles

def analyze_with_claude(query, articles):
    """Send articles to Claude for analysis"""
    # Format articles into readable text
    article_text = ""
    for i, article in enumerate(articles):
        article_text += f"Article {i+1}: {article['title']}\n{article['description']}\n\n"

    # Ask Claude to analyze them
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a market research analyst. Based on these recent news articles about "{query}", provide:
1. A brief summary of the current landscape
2. Key trends you notice
3. Main players or companies mentioned
4. Any opportunities or risks

Articles:
{article_text}"""
            }
        ]
    )
    return message.content[0].text

# --- Streamlit UI ---
st.title("AI Market Research Tool")
st.write("Enter a company name or industry to generate a research brief.")

query = st.text_input("What do you want to research?", placeholder="e.g. Salesforce, AI startups, electric vehicles")

if st.button("Generate Report"):
    if query:
        with st.spinner("Fetching news and analyzing..."):
            articles = get_news(query)
            if not articles:
                st.error("No articles found. Try a different search term.")
            else:
                analysis = analyze_with_claude(query, articles)
                st.subheader(f"Research Brief: {query}")
                st.write(analysis)
    else:
        st.warning("Please enter a search term.")