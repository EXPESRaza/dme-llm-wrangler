# THE PROMPT WRANGLER

Extract structured data from messy clinical notes using OpenAI's LLMs.

## Features

- Streamlit UI for clinical note processing
- Extract structured JSON using OpenAI's GPT models
- Live prompt tuning + model config
- Shows token usage and response time

## Getting Started

```bash
git clone https://github.com/your-org/dme-llm-wrangler.git
cd dme-llm-wrangler
python -m venv .venv
source .venv\Scripts\activate # on Windows
pip install -r requirements.txt
```

## Setup your OpenAI key

Create a `.env` file:

```env
OPENAI_API_KEY=your-key-here
```

## Run the app

```bash
streamlit run app.py
```

## Suggested System Prompt

You are a helpful assistant that extracts structured data in **valid JSON format** from messy clinical text notes.

Always return only a JSON object—no explanations, no extra text.

Use this suggested JSON schema:
```json
{
"device": string,
"mask_type": string (optional),
"add_ons": [string] (optional),
"qualifier": string (optional),
"ordering_provider": string,
"diagnosis": string (optional),
"SpO2": string (optional),
"usage": [string] (optional),
"type": string (optional),
"features": [string] (optional),
"mobility_status": string (optional),
"product": string (optional),
"components": [string] (optional),
"compliance_status": string (optional)
}
```
Only include fields relevant to the note. Omit fields not mentioned.

### Sample System Prompt Schema
```json
{
"device": "",
"mask_type": "",
"add_ons": [],
"qualifier": "",
"ordering_provider": ""
}
```
### Sample User Prompt to test above System Prompt Schema

"Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron."

## Application UI
![image](https://github.com/user-attachments/assets/a083e96c-da45-4c2f-99c6-fccd595e1b9d)


