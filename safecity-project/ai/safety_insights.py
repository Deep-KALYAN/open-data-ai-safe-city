# ai/safety_insights.py
from utils.llm import call_llm
from ai.prompt_builder import build_department_prompt
from data_processing.ai_features import get_department_ai_features

# ai/safety_insights.py

import pandas as pd



def generate_safety_insight(
    df_risk,
    dept_code,
    year,
    provider="ollama",
):
    """
    Generate AI-based safety advice for a department and year.
    """

    # Filter department + year
    df = df_risk[
        (df_risk["Code_departement"] == dept_code)
        & (df_risk["annee"] == year)
    ]


    if df.empty:
        return "No data available for the selected department and year."

    row = df.iloc[0]

    prompt = f"""
You are a public safety expert.

Department: {department}
Year: {year}

Crime indicators (normalized):
- Violent crime risk: {row.get("Violent", 0):.2f}
- Property crime risk: {row.get("Property", 0):.2f}
- Drug-related crime risk: {row.get("Drugs", 0):.2f}
- Financial crime risk: {row.get("Financial", 0):.2f}

Overall risk score: {row.get("risk_score_norm", 0):.2f}
Risk level: {row.get("risk_level", "Unknown")}

Write:
1. A short risk summary
2. Main safety concerns
3. Practical safety advice for citizens
"""

    return call_llm(prompt, provider=provider)

# def generate_safety_insight(dept_code, dept_name, year, provider="ollama"):
#     stats = get_department_ai_features(dept_code, year)

#     if not stats:
#         return "No data available for this department and year."

#     prompt = build_department_prompt(dept_name, year, stats)

#     response = call_llm(
#         prompt=prompt,
#         provider=provider,
#         temperature=0.4,
#     )

#     return response
