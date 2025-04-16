def extract_structured_data(client, system_prompt, user_prompt, model, temperature, max_tokens):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"} 
    )
    usage = response.usage if hasattr(response, 'usage') else 'N/A'
    return response.choices[0].message.content.strip(), usage
