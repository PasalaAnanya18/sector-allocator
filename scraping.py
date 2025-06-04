import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("NEWSDATA_API_KEY")

api = NewsDataApiClient(API_KEY)

def build_query(keywords):
    return ' OR '.join(keywords)

def fetch_headlines(query, category='business'):
    response = api.news_api(q=query, category=category, language='en')
    headlines = []
    for item in response.get('results', []):
        if 'title' in item:
            headlines.append(item['title'])
    
    return headlines[:20]

def collect_all_headlines(sector_keywords):
    all_headlines = []
    for sector, keywords in sector_keywords.items():
        query = build_query(keywords)
        headlines = fetch_headlines(query)
        all_headlines.append({'sector': sector, 'headlines': headlines})
    return pd.DataFrame(all_headlines)