from utils.llm import call_llm
import pandas as pd


def generate_comparison_insight(
    df_risk: pd.DataFrame,
    dept_a_code: str,
    dept_a_name: str,
    dept_b_code: str,
    dept_b_name: str,
    year: int,
    provider: str = "ollama",
):
    """
    Generate AI comparison between two departments.
    """

    a = df_risk[
        (df_risk["Code_departement"] == dept_a_code)
        & (df_risk["annee"] == year)
    ].iloc[0]

    b = df_risk[
        (df_risk["Code_departement"] == dept_b_code)
        & (df_risk["annee"] == year)
    ].iloc[0]

    prompt = f"""
You are a public safety analyst.

Compare crime risks between two French departments for the year {year}.

Department A:
- Name: {dept_a_name}
- Risk score: {a['risk_score_norm']}
- Risk level: {a['risk_level']}
- Violent crime: {a.get('Violent', 0):.2f}
- Property crime: {a.get('Property', 0):.2f}
- Drug crime: {a.get('Drugs', 0):.2f}
- Financial crime: {a.get('Financial', 0):.2f}

Department B:
- Name: {dept_b_name}
- Risk score: {b['risk_score_norm']}
- Risk level: {b['risk_level']}
- Violent crime: {b.get('Violent', 0):.2f}
- Property crime: {b.get('Property', 0):.2f}
- Drug crime: {b.get('Drugs', 0):.2f}
- Financial crime: {b.get('Financial', 0):.2f}

Tasks:
1. State which department is safer overall.
2. Explain the main crime differences.
3. Highlight specific risks for each department.
4. Provide safety recommendations for residents and visitors.
5. Keep the explanation clear and concise.
"""

    return call_llm(prompt, provider=provider)
