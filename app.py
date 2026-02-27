import streamlit as st
import requests

API_URL = "http://localhost:8000/profiles"

st.title("Nutrition AI Agent — User Profile")


with st.form("profile_form"):

    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    st.subheader("Height")
    feet, inches = st.columns(2)
    with feet: 
        heightFt = st.number_input("Feet", min_value=1, max_value=8, value=5)
    with inches: 
        heightIn = st.number_input("Height (inches)", min_value=0, max_value=11, value=0)
    weight = st.number_input("Weight (lbs)", min_value=40.0, max_value=1000.0, value=40.0)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    goal = st.selectbox("Goal", ["Weight Loss", "Maintenance", "High Protein", "Gluten Free"])
    dietary = st.multiselect("Dietary Preferences", ["Vegetarian", "Vegan", "Pescaterian", "Low Carb", "Keto"])
    allergies = st.multiselect("Allergies", ["Nuts", "Dairy", "Gluten", "Soy", "Eggs"])
    medical = st.multiselect("Medical Conditions", ["Diabetes", "Hypertension", "Celiac", "High Cholesterol"])
    budget = st.number_input( "Weekly Grocery Budget ($)", min_value=20, max_value=500, value=100,step=10)
    cooking_time = st.selectbox("Cooking Time (minutes)", ["Short (< 30)", "Medium (30-60)", "Long(>60)"])

    submitted = st.form_submit_button("Submit Profile")

if submitted:
    payload = {
        "age": int(age),

        # match new US-unit schema
        "height_feet": int(heightFt),
        "height_inches": int(heightIn),
        "weight_lbs": float(weight),

        "gender": gender,
        "goal": goal,
        "dietary_preferences": dietary or [],
        "allergies": allergies or [],
        "medical_conditions": medical or [],
        "budget_level": budget,
        "cooking_time": cooking_time,
    }

    try:
        r = requests.post(API_URL, json=payload)
        r.raise_for_status()
        st.success("Profile saved successfully!")
    except requests.exceptions.HTTPError as e:
        st.error(f"Failed to save profile: {e} - {r.text}")