import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_country = data['le_country']
le_edlevel = data['le_edlevel']
le_sexuality = data['le_sexuality']
le_gender = data['le_gender']
le_employment = data['le_employment']

def show_predict_page():
    st.title('Software Developer Salary Prediction : 2021')

    st.write("""## We need some information to predict the salary""")
    st.write("""### - Made with ❤️ By Vinayak Aneesh!""")

    countries = (

        'Sweden', 
        'Spain', 
        'Germany', 
        'Canada', 
        'Other Countries',
       'United Kingdom of Great Britain and Northern Ireland',
       'Russian Federation', 
       'Israel', 
       'Turkey', 
       'Ukraine',
       'United States of America', 
       'France', 
       'Brazil', 
       'Bulgaria',
       'Greece', 
       'Italy', 
       'Netherlands', 
       'Poland', 
       'Switzerland',
       'Hungary', 
       'Pakistan', 
       'Nigeria', 
       'Bangladesh', 
       'Romania',
       'Sri Lanka', 
       'India', 
       'Croatia', 
       'Denmark', 
       'Ireland', 
       'Egypt',
       'Colombia', 
       'Australia', 
       'Belgium', 
       'Indonesia',
       'Portugal', 
       'Finland', 
       'Argentina',
       'Japan', 
       'Austria', 'South Africa', 'Norway', 'Serbia',
       'Czech Republic', 'China', 'Mexico', 'New Zealand'
    )

    education = (
        "Master's", "Bachelor’s", "Professional", "No Degree"
    )

    employment = (
        'Full Time Employee', 'Not willing to share', 'Part Time Employee',
       'Freelancer', 'Retired Employee'
    )

    gender = (
        'Man' ,'Woman' ,'Unidentified / Not Disclosing'
    )

    sexuality = (
        'Straight' ,'Prefer to self-describe' ,'LGBTQ'

    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)
    employment = st.selectbox("Current type of Employment", employment)
    gender = st.selectbox("Gender", gender)
    sexuality = st.selectbox("Sexuality", sexuality)

    ok = st.button("Calculate Salary")
    if ok:
        #X = np.array([['Germany', 'Bachelor’s', 10.0, 'Full Time Employee','Unidentified / Not Disclosing', 'Straight']])
        X = np.array([[country, education, experience, employment, gender, sexuality ]])
        X[:,0] = le_country.transform(X[:,0])
        X[:,1] = le_edlevel.transform(X[:,1])
        X[:,3] = le_employment.transform(X[:,3])
        X[:,4] = le_gender.transform(X[:,4])
        X[:,5] = le_sexuality.transform(X[:,5])
        
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")