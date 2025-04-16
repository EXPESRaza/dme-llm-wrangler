from typing import Tuple, Dict

def extract_structured_data(
    client, system_prompt: str, user_prompt: str, model: str, temperature: float, max_tokens: int
) -> Tuple[str, Dict]:
    """
    Extract structured data from clinical notes using an LLM.

    Args:
        client: OpenAI client instance.
        system_prompt: The system prompt to guide the LLM.
        user_prompt: The clinical note to process.
        model: The LLM model to use.
        temperature: Sampling temperature for the LLM.
        max_tokens: Maximum number of tokens for the response.

    Returns:
        A tuple containing the JSON response and token usage statistics.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    usage = response.usage if hasattr(response, 'usage') else {}
    return response.choices[0].message.content.strip(), usage