import ollama

def query_ollama(prompt: str, model: str = "mistral") -> str:
    response = ollama.generate(model=model, prompt=prompt)
    return response["response"]

print(query_ollama("What is the capital of France?"))