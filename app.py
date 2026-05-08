import streamlit as st

st.set_page_config(page_title="Deprescribing Pilot", page_icon="💊")

st.title("💊 Deprescribing Pilot - Diuretics in Older Adults")
st.markdown("**Criteria:** Concomitant use of 2+ diuretics in arterial hypertension")

with st.form("patient_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=120, value=70)

    with col2:
        chronic_diseases = st.multiselect(
            "Chronic diseases",
            ["Diabetes", "CKD", "Heart Failure", "COPD", "Arthritis", "Cancer", "Thyroid",  "Other"],
            default=[]
        )

    hypertension = st.checkbox("Hypertension diagnosis", value=False)

    st.subheader("Diuretics")
    col3, col4 = st.columns(2)
    with col3:
        furosemide = st.checkbox("Furosemide", value=False)
    with col4:
        hydrochlorothiazide = st.checkbox("Hydrochlorothiazide", value=False)

    other_diuretics = st.text_input("Other diuretics (comma-separated)", placeholder="e.g., spironolactone, bumetanide")

    other_meds = st.text_area("Other medications (optional)", placeholder="List other medications...")

    submitted = st.form_submit_button("Evaluate", type="primary")

if submitted:
    # Count diuretics
    diuretic_count = 0
    if furosemide:
        diuretic_count += 1
    if hydrochlorothiazide:
        diuretic_count += 1
    if other_diuretics.strip():
        other_diuretic_list = [d.strip() for d in other_diuretics.split(",") if d.strip()]
        diuretic_count += len(other_diuretic_list)

    # Check criteria
    age_criteria = age >= 75 or (age >= 65 and len(chronic_diseases) > 2)
    criteria_met = age_criteria and hypertension and diuretic_count >= 2

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Age", f"{age} years")
        st.metric("Chronic diseases", len(chronic_diseases))
    with col_b:
        st.metric("Hypertension", "Yes" if hypertension else "No")
        st.metric("Diuretics", diuretic_count)

    st.divider()

    if criteria_met:
        st.error("⚠️ Deprescribing Criteria MET")
        st.markdown("""
        ### Recommendation

        **Consider deprescribing one diuretic:**

        1. Review if both diuretics are necessary for blood pressure control
        2. Consider continuing only one diuretic (preferably the one with better response)
        3. Monitor blood pressure after adjustment
        4. Assess renal function and electrolytes
        5. Consider consulting cardiology if heart failure is present

        **Rationale:** Concomitant use of multiple diuretics in older adults increases risk of:
        - Electrolyte disturbances (hypokalemia, hyponatremia)
        - Renal impairment
        - Orthostatic hypotension
        - Falls
        """)
    else:
        st.success("✓ Criteria NOT met")

        reasons = []
        if not age_criteria:
            if age < 65:
                reasons.append("Age < 65 years")
            elif len(chronic_diseases) <= 2:
                reasons.append("Age 65-74 with ≤ 2 chronic diseases")
        if not hypertension:
            reasons.append("No hypertension diagnosis")
        if diuretic_count < 2:
            reasons.append(f"Only {diuretic_count} diuretic(s) (need ≥2)")

        st.info(f"Reason(s): {', '.join(reasons)}")