import streamlit as st
import time
import openai
import json
from utils.extractors import extract_structured_data
from config.settings import get_openai_client

st.set_page_config(page_title="DME LLM Wrangler", layout="wide")
st.title("The Prompt Wrangler")

with st.sidebar:
    st.header("LLM Configuration")
    model = "gpt-3.5-turbo"
    temperature = st.slider("Temperature", 0.0, 1.0, 0.9)
    max_tokens = st.slider("Max Tokens", 100, 2000, 1400)

system_prompt = st.text_area(
    "System Prompt",
    """You are a helpful assistant that extracts structured data in **valid JSON format** from messy clinical text notes.

Always return only a JSON object—no explanations, no extra text.
"""
, height=200)

user_input = st.text_area("Paste Clinical Note Here")

if st.button("Extract Structured Data") and user_input:
    client = get_openai_client()
    with st.spinner("Calling the LLM..."):
        start = time.time()
        try:
            response, usage = extract_structured_data(
                client, system_prompt, user_input, model, temperature, max_tokens
            )
            st.code(response, language="json")
            st.success("Done!")
            st.caption(f"Response time: {round(time.time() - start, 2)}s | Prompt tokens: {usage.prompt_tokens} | Completion tokens: {usage.completion_tokens} | Total tokens used: {usage.total_tokens}")
        except Exception as e:
            st.error(f"Error: {e}")
