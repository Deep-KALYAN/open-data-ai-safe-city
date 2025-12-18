from data_ingestion.crime import load_crime_data


def test_crime_data_loads():
    df = load_crime_data()

    # 🔍 TEMP DEBUG (remove later)
    print(df.head())
    print(df.columns.tolist()[:10])

    assert not df.empty
    assert len(df.columns) > 5

    
