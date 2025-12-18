from utils.llm import call_llm

def ask_question(question: str, context: str):
    prompt = f"""
Context:
{context}

Question:
{question}
"""
    return call_llm(prompt, model_key="narrative")
