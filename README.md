🦠 Norovirus Health Data Simulator
This project simulates realistic Norovirus-related health data and stores it in both CSV and SQLite formats. It's designed for use in data analysis, epidemiological studies, dashboard development, and database-driven applications.

🔍 Features
Synthetic Data Generation: Creates over 17,000 individual health records.

Location-Specific Simulation:
Countries: India, USA, China, Brazil, UK.
Indian cities focus on South India (Kerala, Tamil Nadu, etc.).

Realistic Health Conditions:
Includes flags for heart disease, diabetes, COPD, high blood pressure, and mortality/recovery.
Date Simulation: Report dates range from 1968 to March 2025.
Gender & Age Distribution: Varied age range and gender proportions.

Data Export:
CSV file: norovirus_cases.csv
SQLite database: norovirus.db

📊 Database Tables
cases: Main dataset of individual health records.
gender_distribution: Gender-wise case counts.
hospitalization: Annual hospitalization records (from 2021 onward).

🧪 Use Cases
Testing data pipelines
Practicing SQL queries
Creating dashboards (e.g., Flask, Dash, Power BI)
Machine learning dataset prototyping

🛠️ Built With
Python
Pandas
NumPy
SQLAlchemy
SQLite

🚀 Getting Started

To simulate the data, run:
bash
Copy
Edit
python simulate_data.py

This will generate:
norovirus_cases.csv
norovirus.db with 3 SQLite tables
