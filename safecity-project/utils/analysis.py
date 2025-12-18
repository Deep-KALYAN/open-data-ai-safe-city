def trend_prompt(stats: dict) -> str:
    return f"""
You are an urban safety analyst.

Crime statistics:
{stats}

Tasks:
1. Identify notable trends
2. Highlight anomalies
3. Provide interpretation for decision-makers
"""
