import streamlit as st
import numpy
import torch
import pandas as pd
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from sectorKeywords import sector_keywords
from scraping import build_query, fetch_headlines, collect_all_headlines
from sentimentAnalysis import get_sentiment
from sectorAllocation import allocate_sector

st.set_page_config(page_title="Sector Allocator", layout="wide")
st.title("Sector Allocation Tool")
st.sidebar.header("Settings")
st.sidebar.subheader("Select Sectors")
selected_sectors = st.sidebar.multiselect(
    "Choose sectors to analyze",
    options=list(sector_keywords.keys()),
    default=None)
if st.sidebar.button("Fetch Headlines"):
    with st.spinner("Fetching headlines..."):
        sector_keywords_selected = {sector: sector_keywords[sector] for sector in selected_sectors}
        all_headlines = collect_all_headlines(sector_keywords_selected)
        st.session_state.headlines = all_headlines
if 'headlines' in st.session_state:
    st.subheader("Fetched Headlines")
    for sector, headlines in st.session_state.headlines.groupby('sector'):
        st.write(f"### {sector}")
        for headline in headlines['headlines'].values[0]:
            st.write(f"- {headline}")

    if st.sidebar.button("Analyze Sentiment"):
        with st.spinner("Analyzing sentiment..."):
            model = AutoModelForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', low_cpu_mem_usage=False)
            model.to_empty(device=torch.device('cpu'))
            model.load_state_dict(AutoModelForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone').state_dict(), assign=True)
            tokenizer = AutoTokenizer.from_pretrained('yiyanghkust/finbert-tone')
            analyser = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
            sentiment_results = get_sentiment(st.session_state.headlines, analyser)
            st.session_state.sentiment_results = sentiment_results

        if 'sentiment_results' in st.session_state:
            st.subheader("Sentiment Analysis Results")
            st.dataframe(st.session_state.sentiment_results)
            
            if st.sidebar.button("Allocate Sectors"):
                with st.spinner("Allocating sectors..."):
                    allocation = allocate_sector(st.session_state.sentiment_results)
                    st.session_state.allocation = allocation

            if 'allocation' in st.session_state:
                st.subheader("Sector Allocation")
                st.write(st.session_state.allocation)
                st.bar_chart(st.session_state.allocation)
                st.write("### Allocation Weights")
                st.dataframe(pd.DataFrame(st.session_state.allocation.items(), columns=['Sector', 'Weight (%)']))
    else:
        st.info("Please select sectors and fetch headlines to start the analysis.")
        st.sidebar.info("Use the sidebar to select sectors and fetch headlines.")
