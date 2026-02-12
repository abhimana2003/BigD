import streamlit as st
import requests

API_URL = "http://localhost:8000/profiles"

st.title("Nutrition AI Agent — User Profile")

with st.form("profile_form"):
    # Numeric fields
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    height = st.number_input("Height (cm)", min_value=50.0, value=170.0)
    weight = st.number_input("Weight (kg)", min_value=20.0, value=70.0)

    # Select boxes
    gender = st.selectbox("Gender", ["female", "male", "other"])
    goal = st.selectbox("Goal", ["weight loss", "maintenance", "high protein", "gluten free"])
    dietary = st.multiselect("Dietary Preferences", ["vegetarian", "vegan", "pescaterian", "low carb", "keto"])
    allergies = st.multiselect("Allergies", ["nuts", "dairy", "gluten", "soy", "eggs"])
    medical = st.multiselect("Medical Conditions", ["diabetes", "hypertension", "celiac", "high cholesterol"])
    budget = st.selectbox("Budget Level", ["low", "medium", "high"])
    cooking_time = st.selectbox("Cooking Time", ["short (<30 mins)", "medium (30-60 min)", "long(>60 mins)"])

    submitted = st.form_submit_button("Submit Profile")

if submitted:
    # Build payload
    payload = {
        "age": int(age),
        "height_cm": float(height),
        "weight_kg": float(weight),
        "gender": gender,
        "goal": goal,
        "dietary_preferences": dietary if dietary else [],
        "allergies": allergies if allergies else [],
        "medical_conditions": medical if medical else [],
        "budget_level": budget,
        "cooking_time": cooking_time,
    }

    try:
        # POST to FastAPI backend
        r = requests.post(API_URL, json=payload)
        r.raise_for_status()
        st.success("Profile saved successfully!")
    except requests.exceptions.HTTPError as e:
        # Show full error message
        st.error(f"Failed to save profile: {e} - {r.text}")
