import streamlit as st

st.title("BMI Calculator")

# --- Height ---
height_unit = st.radio("Height unit", ["feet", "meters"])
height = st.number_input("Enter your height", min_value=0.0, value=5.5, step=0.1)

# --- Weight ---
weight_unit = st.radio("Weight unit", ["lbs", "kg"])
weight = st.number_input("Enter your weight", min_value=0.0, value=130.0, step=5.0)

# --- Convert to metric ---
if height_unit == "feet":
    height_m = height * 0.3048
else:
    height_m = height

if weight_unit == "lbs":
    weight_kg = weight * 0.453592
else:
    weight_kg = weight

# --- Calculate BMI ---
if height_m > 0:
    bmi = weight_kg / height_m ** 2
    st.subheader(f"Your BMI is {bmi:.1f}")
else:
    st.write("Please enter a height greater than 0.")