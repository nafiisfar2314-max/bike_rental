from timeit import main
from unittest import result

import streamlit as st
import pandas as pd
import pickle
import numpy as np
import time
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_bike = pickle.load(open(os.path.join(BASE_DIR, 'model/rental_bike.pkl'), 'rb'))

st.set_page_config(page_title="Bike Sharing Prediction", page_icon="🚲", layout="centered")

def predict_bike_rentals():
    st.title("Bike Sharing Prediction")
    st.write("""
        This app predicts the number of bike rentals based on various parameters. Please fill in the details below to get your prediction.
        Data obtained from the UCI Machine Learning Repository: [Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)
                    """)
    
    st.set_page_config(
    page_title="Bike Sharing Prediction",
    page_icon="🚲",
    layout="wide",          # "centered" atau "wide"
    initial_sidebar_state="expanded"  # "expanded", "collapsed", "auto"
)

    st.image("public./rental.jpg", caption="Bike Sharing Prediction", use_container_width=True)

    st.sidebar.header("Input Parameters:")
    with st.sidebar.expander("ℹ️ Column Description (click to expand)"):
        
        st.markdown("#### 📅 Time")
        st.markdown("""
        - **yr** → Tahun (0 = 2011, 1 = 2012)
        - **mnth** → Bulan (1–12)
        - **hr** → Jam (0–23)
        - **weekday** → Hari dalam seminggu (0=Minggu ... 6=Sabtu)
        - **holiday** → Hari libur nasional (1=Ya, 0=Tidak)
        """)

        st.markdown("#### 🌤️ Wearher")
        st.markdown("""
        - **season** → Season (1=Winter, 2=Spring, 3=Summer, 4=Fall)
        - **weathersit** → Kondisi cuaca:
            - 1 = Clear
            - 2 = Mist/Cloudy
            - 3 = Light Rain/Light Snow
            - 4 = Heavy Rain/Heavy Snow
        - **temp** → Air temperature (normalized 0–1)
        - **hum** → Humidity (normalized 0–1)
        - **windspeed** → Wind speed (normalized 0–1)
        """)

        season = st.sidebar.selectbox("Season", [1, 2, 3, 4])
        if season == 1:
            st.sidebar.write("Winter")
        elif season == 2:
            st.sidebar.write("Spring")
        elif season == 3:
            st.sidebar.write("Summer")
        elif season == 4:
            st.sidebar.write("Fall")

        yr = st.sidebar.selectbox("Year", [0, 1])
        if yr == 0:
            st.sidebar.write("2011")
        elif yr == 1:
            st.sidebar.write("2012")

        mnth = st.sidebar.slider("Month", 1, 12, 6)
        bulan_nama = ['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec']
        st.sidebar.write(bulan_nama[mnth - 1])

        hr = st.sidebar.slider("Hour", 0, 23, 12)
        if hr in [7, 8, 9]:
            st.sidebar.write("Morning Rush Hour")
        elif hr in [16, 17, 18, 19]:
            st.sidebar.write("Evening Rush Hour")
        elif 0 <= hr <= 5:
            st.sidebar.write("Late Night / Early Morning")
        else:
            st.sidebar.write("Regular Hour")

        holiday = st.sidebar.selectbox("Holiday", [0, 1])
        if holiday == 0:
            st.sidebar.write("Not a Holiday")
        elif holiday == 1:
            st.sidebar.write("Holiday")

        weekday = st.sidebar.selectbox("Weekday", [0, 1, 2, 3, 4, 5, 6])
        hari_nama = ['Sunday','Monday','Tuesday','Wednesday',
                    'Thursday','Friday','Saturday']
        st.sidebar.write(hari_nama[weekday])

        weathersit = st.sidebar.selectbox("Weather Situation", [1, 2, 3, 4])
        if weathersit == 1:
            st.sidebar.write("Clear / Partly Cloudy")
        elif weathersit == 2:
            st.sidebar.write("Mist / Cloudy")
        elif weathersit == 3:
            st.sidebar.write("Light Rain / Light Snow")
        elif weathersit == 4:
            st.sidebar.write("Heavy Rain / Heavy Snow")

        temp = st.sidebar.slider("Temperature (normalized)", 0.0, 1.0, 0.5)
        temp_celsius = temp * (39 - (-8)) + (-8)
        st.sidebar.write(f"≈ {temp_celsius:.1f}°C")
        if temp_celsius < 10:
            st.sidebar.write("Cold")
        elif temp_celsius < 25:
            st.sidebar.write("Comfortable")
        else:
            st.sidebar.write("Hot")

        hum = st.sidebar.slider("Humidity (normalized)", 0.0, 1.0, 0.5)
        if hum < 0.3:
            st.sidebar.write("Low Humidity")
        elif hum < 0.7:
            st.sidebar.write("Moderate Humidity")
        else:
            st.sidebar.write("High Humidity")

        windspeed = st.sidebar.slider("Windspeed (normalized)", 0.0, 1.0, 0.2)
        if windspeed < 0.2:
            st.sidebar.write("Calm")
        elif windspeed < 0.4:
            st.sidebar.write("Breezy")
        else:
            st.sidebar.write("Windy")
            

        data = {
            'season'    : season,
            'yr'        : yr,
            'mnth'      : mnth,
            'hr'        : hr,
            'holiday'   : holiday,
            'weekday'   : weekday,
            'weathersit': weathersit,
            'temp'      : temp,
            'hum'       : hum,
            'windspeed' : windspeed
        }
        input_data = pd.DataFrame([data])
        st.write("### 📊  Input Data Summary")
        st.write(input_data)

    if st.sidebar.button("Predict"):
        with st.spinner("Predicting..."):
            time.sleep(2)
            prediction = model_bike.predict(input_data)
            hasil = max(0, int(round(prediction[0])))
            

            # Tentukan status berdasarkan hasil
            if hasil < 50:
                status = "🟢 LOW"
            elif hasil < 200:
                status = "🟡 MODERATE"
            else:
                status = "🔴 HIGH"

            st.success(f"🚲 Predicted bike rentals: **{hasil} bikes**")

            # ── Metric Cards ──────────────────────────────────
            col1, col2, col3 = st.columns(3)

            with st.container(border=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Predicted Rentals", f"{hasil} bikes")
                with col2:
                    st.metric("Temperature", f"{temp_celsius:.1f}°C")
                with col3:
                    st.metric("Demand Status", status)

            # ── Kategori Detail ───────────────────────────────
            if hasil < 50:
                st.info("📊 Category: LOW DEMAND — Fleet can be reduced")
            elif hasil < 200:
                st.warning("📊 Category: MODERATE DEMAND — Normal fleet size")
            else:
                st.error("📊 Category: HIGH DEMAND — Increase fleet!")


def about():
    st.title("About this App")
    st.write("""
    # ## Welcome to my Machine Learning Dashboard 🚲

    This dashboard was created by **[Nafiis Farhan](https://www.linkedin.com/in/nafiis-farhan-0103b4294/)**.

    ---

    ### What does this app do?
    This is a machine learning-based application that predicts the number of bike rentals
    based on weather conditions and time-related factors such as season, temperature,
    humidity, and hour of the day.

    The model was trained on the **UCI Bike Sharing Dataset**, using the XGBoost algorithm,
    achieving an R² score of **0.95** — meaning it explains 95% of the variation in
    bike rental demand.

    ### Why was this built?
    This project was developed as part of a data science portfolio to demonstrate
    an end-to-end machine learning workflow: from exploratory data analysis,
    feature engineering, model comparison, hyperparameter tuning, to deployment.

    ---

    **Disclaimer:** This app is for educational and portfolio purposes only.
    Predictions are based on historical data and should not be used as the sole
    basis for real-world operational decisions.
    """)


def developer_info():
    st.title("👨‍💻 Developer Information")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/200", caption="Nafiis Farhan")
    
    with col2:
        st.markdown("""
        ### Nafiis Farhan
        **Data Science Enthusiast**

        📧 Email: your.email@example.com  
        💼 LinkedIn: [nafiis-farhan](https://www.linkedin.com/in/nafiis-farhan-0103b4294/)  
        🐙 GitHub: [github.com/nafiis-farhan](https://github.com/nafiis-farhan)
        """)
        st.markdown("---")
        
        st.markdown("""
    ### About This Project
    This application was built using **Streamlit**, a Python framework for creating
    interactive web applications with minimal code.

    **Tech Stack:**
    - 🐍 Python
    - 🐼 Pandas & NumPy for data processing
    - 🌳 XGBoost for the prediction model
    - 🎨 Streamlit for the web interface
    - 📊 Matplotlib & Seaborn for visualization
                
      **Project Workflow:**
    1. Exploratory Data Analysis (EDA)
    2. Data Preprocessing & Feature Engineering
    3. Model Comparison (Linear Regression, Decision Tree, Random Forest, XGBoost)
    4. Hyperparameter Tuning with GridSearchCV
    5. Model Deployment with Streamlit

    Thank you for visiting this app — feel free to reach out for collaborations or feedback!
    """)
        
def main():
    st.sidebar.title("🧭 Navigation")
    
    app_mode = st.sidebar.selectbox(
        "Choose a page",
        ["🚲 Bike Rental Prediction", "ℹ️ About this App", "👨‍💻 Developer Information"]
    )

    st.sidebar.markdown("---")

    if app_mode == "🚲 Bike Rental Prediction":
         predict_bike_rentals()
    elif app_mode == "ℹ️ About this App":
        about()
    elif app_mode == "👨‍💻 Developer Information":
        developer_info()


if __name__ == "__main__":
        main()
