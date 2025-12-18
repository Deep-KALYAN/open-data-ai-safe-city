# ai/prompt_builder.py

def build_department_prompt(dept_name, year, stats):
    """
    stats = dict with keys:
    - risk_level
    - risk_score
    - category_breakdown (dict)
    - trend (string)
    """

    categories = "\n".join(
        [f"- {k}: {v:.2f} per 1,000 inhabitants" for k, v in stats["category_breakdown"].items()]
    )

    prompt = f"""
You are a public safety analyst.

Analyze the crime situation for the following French department.

Department: {dept_name}
Year: {year}

Overall risk level: {stats['risk_level']}
Risk score: {stats['risk_score']:.2f}

Crime breakdown:
{categories}

Trend:
{stats['trend']}

Provide:
1. A short situation summary
2. Key risks
3. Practical safety advice for citizens
4. A neutral, non-alarmist tone

Limit to 150 words.
"""
    return prompt
