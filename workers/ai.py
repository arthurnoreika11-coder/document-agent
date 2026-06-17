import ollama

SYSTEM_PROMT = """
You are a legal document analyser, given the text of a legal document. 
Produce a structed agents.md file in the following exact format:

# AGENTS.MD - Document Summary

## Document Type
[In a single sentece, specify the type of the document, e.g., Contract, Agreement, NDA, etc.]

## Parties Involved
[Bullet list of each party involved in the document, including their registered details, roles and responsibilities.]

## Key Dates and Deadlines
[Bullet list of all important dates and deadlines mentioned in the document, including their significance.]

## Defined Terms
[Bullet list of all defined terms used in the document, along with their definitions.]

## Obligations and Responsibilities
### [Party Name]
[List of obligations and responsibilities of the party, including any specific actions they are required to take, deliverables, and timelines.]
"""

def stream_agents(markdown: str, model: str = "mistral"):
    promtp = f"{SYSTEM_PROMT}\n\n{markdown}"
    stream = ollama.generate(model=model, prompt=promtp, stream=True)
    for chunk in stream:
        yield chunk["response"]


for chunk in stream_agents(markdown_text):
    print(chunk, end="", flush=True)