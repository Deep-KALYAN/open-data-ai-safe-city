from ai.safety_insights import generate_safety_insight

text = generate_safety_insight(
    dept_code="13",
    dept_name="Bouches-du-Rhône",
    year=2022,
    provider="ollama",  # switch to "groq" if needed
)

print(text)
