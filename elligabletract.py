import streamlit as st
import pandas as pd
import requests

# Function to get census tract
def get_census_tract(street, city, state):
    # API request
    url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    params = {
        "address": f"{street}, {city}, {state}",
        "benchmark": "Public_AR_Current",
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()  # Assuming the API returns JSON

# Extract GEOID and BLOCK
def extract_geoid_block(data):
    # Assuming 'data' is a JSON object returned by the Census API and has the correct structure
    geoid = data['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['GEOID']
    block = data['result']['addressMatches'][0]['geographies']['Census Blocks'][0]['BLOCK']
    return geoid, block

# Attempt to load data with error handling
try:
    df = pd.read_csv('https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_HB550_ECT.csv')
except Exception as e:
    df = pd.DataFrame()  # Empty DataFrame as a fallback
    print(f"Error loading data: {e}")

def main():
    st.title("Census Tract Finder")

    street = st.text_input("Street")
    city = st.text_input("City")
    state = st.text_input("State")

    if st.button("Find"):
        try:
            data = get_census_tract(street, city, state)
            geoid, block = extract_geoid_block(data)
            zip_code = data['result']['addressMatches'][0]['addressComponents']['zip']

            st.write(f"GEOID: {geoid}")
            st.write(f"BLOCK: {block}")
            st.write(f"ZIP Code: {zip_code}")

            if geoid in df['GEOID'].values:
                st.write("This is an eligible location based on MD HB 550")
            else:
                st.write("This is NOT an eligible location based on MD HB 550")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
