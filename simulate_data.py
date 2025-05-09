import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine

def simulate_data(num_records=17839):
    np.random.seed(42)

    # Generate random dates between 1968 and March 2025
    start_date = datetime(1968, 1, 1)
    end_date = datetime(2025, 3, 31)
    date_range = pd.date_range(start=start_date, end=end_date)
    random_dates = np.random.choice(date_range, size=num_records)

    # Define country distribution: India has majority
    countries = ["India", "USA", "China", "Brazil", "UK"]
    country_probs = [0.1231, 0.4663, 0.1241, 0.1111, 0.1754]  # India = 10%

    # Define cities biased toward south India within India
    indian_south_cities = ["Kerala", "Andhra Pradesh", "Karnataka", "Telangana", "Tamilnadu"]
    indian_south_probs = [0.4769, 0.1264, 0.1439, 0.1611, 0.0917]  # Kerala has most

    # For non-India cities (placeholders)
    non_india_cities = {
        "USA": ["New York", "Los Angeles", "Chicago"],
        "China": ["Beijing", "Shanghai", "Guangzhou"],
        "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília"],
        "UK": ["London", "Manchester", "Birmingham"]
    }

    # Generate countries first
    countries_chosen = np.random.choice(countries, size=num_records, p=country_probs)

    # Generate city list based on country
    cities_chosen = []
    for c in countries_chosen:
        if c == "India":
            cities_chosen.append(np.random.choice(indian_south_cities, p=indian_south_probs))
        else:
            cities_chosen.append(np.random.choice(non_india_cities[c]))

    # Simulate the dataset
    data = {
        "Individual_ID": np.arange(1, num_records + 1),
        "Age": np.random.randint(1, 90, size=num_records),
        "Sex": np.random.choice(["Male", "Female"], size=num_records),
        "Has_Heart_Disease": np.random.choice([0, 1], size=num_records, p=[0.8, 0.2]),
        "Has_Diabetes": np.random.choice([0, 1], size=num_records, p=[0.75, 0.25]),
        "Has_COPD": np.random.choice([0, 1], size=num_records, p=[0.9, 0.1]),
        "Has_High_BP": np.random.choice([0, 1], size=num_records, p=[0.85, 0.15]),
        "Country": countries_chosen,
        "City": cities_chosen,
        "Is_Dead": np.random.choice([0, 1], size=num_records, p=[0.96, 0.04]),
        "Is_Recovered": np.random.choice([0, 1], size=num_records, p=[0.65, 0.35]),
        "Report_Date": random_dates
    }

    df = pd.DataFrame(data)

    # Save to CSV file
    df.to_csv("norovirus_cases.csv", index=False)  # <--- This line saves the file as CSV

    # Create SQLite connection
    engine = create_engine("sqlite:///norovirus.db")

    # Save main data to SQLite
    df.to_sql("cases", engine, index=False, if_exists="replace")

    # --- Additional Summary Tables ---

    # 1. Gender Distribution
    gender_df = df.groupby("Sex").size().reset_index(name="cases")
    gender_df.to_sql("gender_distribution", engine, index=False, if_exists="replace")

    # 2. Hospitalizations by Year
    df["Year"] = pd.to_datetime(df["Report_Date"]).dt.year
    hospitalization_df = df.groupby("Year").size().reset_index(name="hospitalizations")
    hospitalization_df = hospitalization_df[hospitalization_df["Year"] >= 2021]
    hospitalization_df.to_sql("hospitalization", engine, index=False, if_exists="replace")

    print("✅ Simulation complete. Data stored in 'norovirus.db' and 'norovirus_cases.csv'")

    return df

if __name__ == "__main__": 
    simulate_data(17839)
