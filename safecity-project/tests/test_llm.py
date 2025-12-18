import sys
from pathlib import Path

# Add project root to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.llm import call_llm

PROMPT = "Say in one sentence what SafeCity does."

def test_ollama():
    print("Testing Ollama (local)...")
    response = call_llm(PROMPT, provider="ollama")
    assert len(response) > 0
    print("Ollama OK ✅")
    print(response)

def test_groq():
    print("Testing Groq (remote)...")
    response = call_llm(PROMPT, provider="groq")
    assert isinstance(response, str), "Groq response is not a string"
    assert len(response.strip()) > 0, "Groq returned empty response"
    print("Groq OK ✅")
    print(response)

# def test_groq():
#     print("Testing Groq (remote)...")
#     response = call_llm(PROMPT, provider="groq")
#     assert len(response) > 0
#     print("Groq OK ✅")
#     print(response)

if __name__ == "__main__":
    test_ollama()
    test_groq()
