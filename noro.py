from flask import Flask, render_template, request, redirect, url_for, flash, jsonify , make_response
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import random
from io import BytesIO
from sqlalchemy import create_engine
import sqlite3
import matplotlib
from flask import jsonify
import os

matplotlib.use('Agg')  # Use non-interactive backend for headless environments


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.secret_key = 'jajal'  # <-- Add this line

# Load data from SQLite database
engine = create_engine("sqlite:///norovirus.db")
df = pd.read_sql("SELECT * FROM cases", engine, parse_dates=["Report_Date"])

@app.route('/')
def home():
    conn = sqlite3.connect("norovirus.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cases")
    total_cases = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM cases WHERE Is_Dead = 1")
    total_deaths = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM cases WHERE Is_Recovered = 1")
    total_recovered = cursor.fetchone()[0]

    active_cases = total_cases - total_deaths - total_recovered

    cursor.execute("SELECT COUNT(*) FROM cases WHERE Has_Diabetes = 1")
    diabetes_cases = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM cases WHERE Has_High_BP = 1")
    high_bp_cases = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "home.html",
        total_cases=total_cases,
        total_deaths=total_deaths,
        total_recovered=total_recovered,
        active_cases=active_cases,
        diabetes_cases=diabetes_cases,
        high_bp_cases=high_bp_cases,
        pie_chart=generate_country_pie(df),
        age_group_pie_chart=generate_age_group_pie(df),
        diabetes_pie_chart=generate_diabetes_pie_chart(df),
        bp_pie_chart=generate_bp_pie_chart(df),
        comorbidity_bar=generate_comorbidity_bar(df),
        sex_chart=generate_sex_pie(df)
    )

# ------------------ CHART GENERATION FUNCTIONS ------------------ #

def generate_graph(data, labels, title, color):
    plt.figure(figsize=(6, 4))
    plt.bar(labels, data, color=color)
    plt.xlabel("Categories")
    plt.ylabel("Count")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf8")

def generate_country_pie(df):
    top_countries = df['Country'].value_counts().nlargest(5)
    plt.figure(figsize=(6, 6))
    plt.pie(top_countries, labels=top_countries.index, autopct='%1.1f%%', startangle=140)
    plt.title("Norovirus Cases Distribution by Country")
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def generate_diabetes_pie_chart(df):
    labels = ['With Diabetes', 'Without Diabetes']
    counts = [df['Has_Diabetes'].sum(), len(df) - df['Has_Diabetes'].sum()]
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Norovirus Cases in People with Diabetes")
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf8")

def generate_bp_pie_chart(df):
    high_bp = df["Has_High_BP"].sum()
    no_bp = len(df) - high_bp
    labels = ["With High Blood Pressure", "Without High Blood Pressure"]
    cases = [high_bp, no_bp]
    colors = ["red", "gray"]
    plt.figure(figsize=(6, 6))
    plt.pie(cases, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title("Norovirus Cases in People with High Blood Pressure")
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf8")

def generate_age_group_pie(df):
    bins = [0, 18, 35, 50, 100]
    labels = ["0-18", "19-35", "36-50", "51+"]
    age_groups = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
    counts = age_groups.value_counts().sort_index()
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140)
    plt.title("Patient Age Group Distribution")
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf8")

def generate_comorbidity_bar(df):
    comorbidities = {
        "Heart Disease": df["Has_Heart_Disease"].sum(),
        "Diabetes": df["Has_Diabetes"].sum(),
        "COPD": df["Has_COPD"].sum()
    }
    return generate_graph(list(comorbidities.values()), list(comorbidities.keys()), "Comorbidities Count", "orange")

def generate_sex_pie(df):
    counts = df["Sex"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140, colors=["skyblue", "lightpink"])
    plt.title("Sex Distribution")
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf8")

def generate_line_chart(y_values, x_labels, title, color):
    plt.figure(figsize=(8, 5))
    plt.plot(x_labels, y_values, marker='o', color=color)
    plt.title(title)
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.grid(True)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def generate_cases_2021_2023(df):
    df['Report_Date'] = pd.to_datetime(df['Report_Date'])
    filtered = df[(df['Report_Date'].dt.year >= 2021) & (df['Report_Date'].dt.year <= 2023)]
    yearly_counts = filtered['Report_Date'].dt.year.value_counts().sort_index()
    return generate_line_chart(yearly_counts.tolist(), yearly_counts.index.astype(str).tolist(), "Cases (2021–2023)", "orange")

def plot_gender_distribution():
    genders = ['Male', 'Female']
    cases = [random.randint(500, 1000), random.randint(600, 1100)]
    plt.figure(figsize=(6,4))
    plt.bar(genders, cases, color=['#6a8ef0', '#f46a8a'])
    plt.title("Gender-wise Norovirus Cases")
    plt.xlabel("Gender")
    plt.ylabel("Cases")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def plot_hospitalization_trend():
    years = ['2021', '2022', '2023']
    hospitalizations = [random.randint(1000, 1500), random.randint(1300, 1600), random.randint(1100, 1700)]
    plt.figure(figsize=(6,4))
    plt.plot(years, hospitalizations, marker='o', color='#fc7f03')
    plt.title("Hospitalization Trends (Year-wise)")
    plt.xlabel("Year")
    plt.ylabel("Hospitalized Patients")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/graphs')
def graphs():
    countries = ['USA', 'India', 'China', 'Brazil', 'UK']
    country_cases = df['Country'].value_counts().reindex(countries).fillna(0)
    country_deaths = df[df['Is_Dead'] == 1]['Country'].value_counts().reindex(countries).fillna(0)

    cities = df[df['Country'] == 'India']['City'].value_counts().nlargest(5)
    city_deaths = df[(df['Country'] == 'India') & (df['Is_Dead'] == 1)]['City'].value_counts().reindex(cities.index).fillna(0)

    age_bins = pd.cut(df['Age'], [0, 18, 35, 50, 100], labels=["0-18", "19-35", "36-50", "51+"])
    age_deaths = df[df['Is_Dead'] == 1].groupby(age_bins).size()
    age_cases = age_bins.value_counts().sort_index()
    survival_rates = (1 - (age_deaths / age_cases)).fillna(0)

    recovery_status = df[df['Is_Dead'] == 0]['Country'].value_counts().reindex(countries).fillna(0)

    death_by_comorbidity = {
        "Heart Disease": df[(df['Has_Heart_Disease'] == 1) & (df['Is_Dead'] == 1)].shape[0],
        "Diabetes": df[(df['Has_Diabetes'] == 1) & (df['Is_Dead'] == 1)].shape[0],
        "COPD": df[(df['Has_COPD'] == 1) & (df['Is_Dead'] == 1)].shape[0],
    }

    return render_template("graphs.html",
                           cases_graph=generate_line_chart(country_cases.tolist(), countries, "Cases Per Country", "blue"),
                           deaths_graph=generate_line_chart(country_deaths.tolist(), countries, "Deaths Per Country", "red"),
                           city_cases_graph=generate_line_chart(cities.tolist(), cities.index.tolist(), "Top 5 States in India (Cases)", "green"),
                           city_deaths_graph=generate_line_chart(city_deaths.tolist(), city_deaths.index.tolist(), "Top 5 States in India (Deaths)", "purple"),
                           survival_rate_graph=generate_line_chart(survival_rates.tolist(), survival_rates.index.tolist(), "Survival Rate by Age Group", "teal"),
                           recovery_graph=generate_line_chart(recovery_status.tolist(), countries, "Recovered Cases by Country", "darkgreen"),
                           death_comorbidity_graph=generate_graph(list(death_by_comorbidity.values()), list(death_by_comorbidity.keys()), "Deaths by Comorbidities", "crimson"),
                           cases_2021_2023=generate_cases_2021_2023(df),
                           gender_distribution_graph=plot_gender_distribution(),
                           hospitalization_graph=plot_hospitalization_trend())

@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/solution')
def solution():
    return render_template('solution.html')

@app.route('/self-check')
def self_check():
    return render_template('self-check.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        type_ = request.form['type']
        message = request.form['message']
        
        print(f"Feedback received: {name}, {email}, {type_}, {message}")

        # Redirect to home after successful submission
        return redirect(url_for('home'))

    # Render the feedback form page
    response = make_response(render_template('feedback.html'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def index():
    return "Welcome to Norovirus Tracker"

if __name__ == '__main__':
    app.run(debug=True)
