def validate(df):
    assert df.isnull().sum().sum() == 0, "Missing values detected"
    assert (df["crime_rate"] >= 0).all(), "Negative crime rates"
