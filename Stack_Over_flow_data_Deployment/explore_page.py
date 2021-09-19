import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def country_clean(names, total):
    country_map = {}
    for i in range(len(names)):
        if names.values[i] >= total:
            country_map[names.index[i]] = names.index[i]
        else:
            country_map[names.index[i]] = 'Other Countries'
    return country_map

def clean_edlevel(x):
        if "Master’s degree" in x:
            return "Master's"
        if "Bachelor’s degree" in x:
            return "Bachelor’s"
        if "doctoral" in x or "Professional" in x:
            return "Professional"
        else:
            return "No Degree"

def clean_employment(x):
        if "Independent contractor" in x:
            return "Freelancer"
        if "Employed full-time" in x:
            return "Full Time Employee"
        if "I prefer not to say" in x:
            return "Not willing to share"
        if "Employed part-time" in x:
            return "Part Time Employee"
        if "Independent contractor" in x:
            return "Contract Employee"
        if "Retired" in x:
            return "Retired Employee"

def clean_years_code(x):
        if "Less than 1 year" in x:
            return 0.5
        if 'More than 50 years' in x:
            return 50
        return float(x)

def clean_sexuality(x):
        if x == 'Straight / Heterosexual':
            return "Straight"
        if x == 'Prefer to self-describe:':
            return "Prefer to self-describe"
        else:
            return "LGBTQ"

def clean_gender(x):
        if 'Man' in x:
            return "Man"
        if 'Woman' in x:
            return 'Woman'
        else:
            return "Unidentified / Not Disclosing"

@st.cache

def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df2 = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly','Gender', 'Sexuality','Ethnicity']]
    df2 = df2.rename({'ConvertedCompYearly' : 'Salary'}, axis = 1)
    df2 = df2[df2['Salary'].notnull()]
    df2 = df2.dropna()
    final_country_map = country_clean(df2.Country.value_counts(), 150)
    df2['Country'] = df2['Country'].map(final_country_map)
    
    df2 = df2[df2['Salary'] <= 340000]
    df2 = df2[df2['Salary'] > 10006]
    df2 = df2[df2['Salary'] != 'Other']

    df2['EdLevel'] = df2['EdLevel'].apply(clean_edlevel)
    df2['Employment'] = df2['Employment'].apply(clean_employment)
    df2['YearsCodePro'] = df2['YearsCodePro'].apply(clean_years_code)
    df2['Sexuality'] = df2['Sexuality'].apply(clean_sexuality) 
    df2['Gender'] = df2['Gender'].apply(clean_gender)

    return df2

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2021
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)