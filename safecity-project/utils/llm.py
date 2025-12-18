import os
from litellm import completion


OLLAMA_MODEL = "ollama/mistral"


def _extract_text(response) -> str:
    """
    Safely extract text from LiteLLM response.
    Raises a clear error if no content is returned.
    """
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"Invalid LLM response format: {response}")

    if content is None or not str(content).strip():
        raise RuntimeError(f"LLM returned empty content: {response}")

    return content.strip()


def call_llm(
    prompt: str,
    provider: str = "ollama",   # "ollama" or "groq"
    temperature: float = 0.3,
) -> str:
    """
    Unified LLM caller using LiteLLM.

    Providers:
    - ollama : local inference (mistral)
    - groq   : hosted inference (llama3)

    Returns:
    - model text output (str)
    """

    messages = [{"role": "user", "content": prompt}]

    # -------------------------
    # Local Ollama (Mistral)
    # -------------------------
    if provider == "ollama":
        response = completion(
            model=OLLAMA_MODEL,
            messages=messages,
            api_base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=temperature,
        )
        return _extract_text(response)

    # -------------------------
    # Groq (LLaMA-3)
    # -------------------------
    if provider == "groq":
        response = completion(
            model="llama-3.1-8b-instant",  # or os.getenv("GROQ_MODEL", "llama3-8b-8192")
            custom_llm_provider="groq",
            messages=messages,
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=temperature,
        )
        return _extract_text(response)

    # -------------------------
    # Safety
    # -------------------------
    raise ValueError(f"Unknown LLM provider: {provider}")


# import os
# from litellm import completion


# # -----------------------------
# # Model configuration
# # -----------------------------

# OLLAMA_MODEL = "ollama/mistral"


# # -----------------------------
# # LLM caller
# # -----------------------------

# def call_llm(
#     prompt: str,
#     provider: str = "ollama",   # "ollama" or "groq"
#     temperature: float = 0.3,
# ) -> str:
#     """
#     Unified LLM caller using LiteLLM.

#     Providers:
#     - ollama : local inference (mistral)
#     - groq   : hosted inference (llama3)

#     Returns:
#     - model text output (str)
#     """

#     messages = [{"role": "user", "content": prompt}]

#     # -------------------------
#     # Local Ollama (Mistral)
#     # -------------------------
#     if provider == "ollama":
#         return completion(
#             model=OLLAMA_MODEL,
#             messages=messages,
#             api_base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
#             temperature=temperature,
#         )["choices"][0]["message"]["content"]

    # -------------------------
    # Groq (LLaMA-3)
    # -------------------------


# import os
# from litellm import completion

# OLLAMA_MODEL = "ollama/mistral"
# GROQ_MODEL = "llama3-8b-8192"#"groq/llama3-70b-8192"#"groq/mixtral-8x7b-32768"

# def call_llm(
#     prompt: str,
#     provider: str = "ollama",  # "ollama" or "groq"
#     temperature: float = 0.3,
# ):
#     """
#     Call LLM via LiteLLM.
#     provider:
#       - 'ollama' → local mistral
#       - 'groq' → hosted mixtral
#     """

#     if provider == "ollama":
#         return completion(
#             model=OLLAMA_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             api_base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
#             temperature=temperature,
#         )["choices"][0]["message"]["content"]

#     if provider == "groq":
#         return completion(
#             model=GROQ_MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             api_key=os.getenv("GROQ_API_KEY"),
#             temperature=temperature,
#         )["choices"][0]["message"]["content"]

#     raise ValueError("Unknown provider")
