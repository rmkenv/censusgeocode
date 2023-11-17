import streamlit as st
import pandas as pd
import requests

# Load data
@st.cache  # Correct decorator
def load_data():
    try:
        url = 'https://raw.githubusercontent.com/user/repo/master/census.csv'  # Ensure the URL is correct
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

df = load_data()

# Get eligible GEOIDs
eligible_geoids = df['GEOID'].astype(str).tolist() if not df.empty else [] 

# Census API function
def get_census_data(street, city, state):
    url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    params = {
        "address": f"{street}, {city}, {state}", 
        "benchmark": "Public_AR_Census2020",
        "vintage": "Census2020_Census2020",
        "layers": "10", 
        "format": "json"
    }  

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'result' not in data:
            raise Exception("No result in response")

        result = data['result']

        if 'addressMatches' not in result or not result['addressMatches']:
            raise Exception("No address matches found")

        address_match = result['addressMatches'][0]

        if 'geographies' not in address_match:
            raise Exception("No geographies found")

        geo = address_match['geographies']['Census Blocks'][0]  # Make sure the key matches the JSON structure

        census_tract = geo.get('TRACT', 'N/A')  # Use get to avoid KeyError
        census_block = geo.get('BLOCK', 'N/A')

        return census_tract, census_block

    except Exception as e:
        st.error(f"Error: {e}")
        return None, None  # Make sure to return after logging error

# Streamlit app
st.title('Census Tract Finder') 

street = st.text_input('Street')
city = st.text_input('City')  
state = st.text_input('State')

if st.button('Find Census Tract'):
    census_tract, census_block = get_census_data(street, city, state)

    if census_tract and census_block:  # Check both values
        st.write(f"Census Tract: {census_tract}")
        st.write(f"Census Block: {census_block}")

        if census_tract in eligible_geoids:
            st.success("Location is eligible")
        else:
            st.error("Location is not eligible")
    else:
        st.error("Could not find census data for the location")
