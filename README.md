# AI Market Research Tool

An AI-powered market research tool that generates detailed company and industry briefs from live news data.

## What it does
Enter any company name or industry — the app pulls recent news articles, Claude AI analyzes them, and you get a structured research brief including executive summary, key trends, major players, opportunities, and risks.

## Tech Stack
- Python / Flask — backend server
- Anthropic Claude API — AI analysis
- NewsAPI — live news article retrieval
- HTML / CSS / JavaScript — custom frontend

## Features
- Real-time news pulling with recency filter (7, 14, or 30 days)
- Adjustable article count (5-20 articles)
- Multi-company comparison support
- Structured 6-section research briefs
- Pacific Northwest themed UI

## Setup
1. Clone the repo
2. Install dependencies: pip3 install flask anthropic requests python-dotenv
3. Create a .env file: ANTHROPIC_API_KEY=your-key-here and NEWS_API_KEY=your-key-here
4. Run: python3 app.py
5. Open http://127.0.0.1:5000

## Built by
Boston Borg — Business Administration and Economics, SPU Class of 2026
