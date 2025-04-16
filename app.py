import streamlit as st
import time
import logging
from utils.extractors import extract_structured_data
from config.settings import get_openai_client

# Constants
DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant that extracts structured data in **valid JSON format** from messy clinical text notes.

Always return only a JSON object—no explanations, no extra text.
"""
DEFAULT_MODEL = "gpt-3.5-turbo"
TEMPERATURE_RANGE = (0.0, 1.0)
MAX_TOKENS_RANGE = (100, 4096)
DEFAULT_TEMPERATURE = 0.9
DEFAULT_MAX_TOKENS = 1400

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def render_system_prompt() -> str:
    """Render the system prompt input area."""
    return st.text_area(
        "System Prompt",
        DEFAULT_SYSTEM_PROMPT,
        height=200,
    )

def render_user_input() -> str:
    """Render the user input text area."""
    return st.text_area("Paste Clinical Note Here")

def validate_inputs(user_input: str) -> bool:
    """Validate user input before making an API call."""
    if not user_input.strip():
        st.error("Clinical note cannot be empty.")
        return False
    return True

def display_response(response: str, usage: dict, start_time: float):
    """Display the LLM response and usage statistics."""
    st.code(response, language="json")
    st.success("Done!")
    st.caption(
        f"Response time: {round(time.time() - start_time, 2)}s | "
        f"Prompt tokens: {getattr(usage, 'prompt_tokens', 'N/A')} | "
        f"Completion tokens: {getattr(usage, 'completion_tokens', 'N/A')} | "
        f"Total tokens used: {getattr(usage, 'total_tokens', 'N/A')}"
    )

def handle_extraction(client, system_prompt, user_input, model, temperature, max_tokens):
    """Handle the LLM extraction process."""
    with st.spinner("Calling the LLM..."):
        start_time = time.time()
        try:
            response, usage = extract_structured_data(
                client, system_prompt, user_input, model, temperature, max_tokens
            )
            display_response(response, usage, start_time)
        except Exception as e:
            st.error("An error occurred while processing your request.")
            logging.error(f"Error: {e}")

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="DME LLM Wrangler", layout="wide")
    st.title("The Prompt Wrangler")

    with st.sidebar:
        st.header("LLM Configuration")
        model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], index=0)
        temperature = st.slider("Temperature", *TEMPERATURE_RANGE, DEFAULT_TEMPERATURE)
        max_tokens = st.slider("Max Tokens", *MAX_TOKENS_RANGE, DEFAULT_MAX_TOKENS)

    system_prompt = render_system_prompt()
    user_input = render_user_input()

    if st.button("Extract Structured Data") and validate_inputs(user_input):
        client = get_openai_client()
        handle_extraction(client, system_prompt, user_input, model, temperature, max_tokens)

if __name__ == "__main__":
    main()