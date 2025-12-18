from data_processing.risk_scoring import build_department_risk_index

df = build_department_risk_index()
print(df.head())
print("Rows:", len(df))
