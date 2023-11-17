import streamlit as st
import pandas as pd
import requests

# Function to get census tract using Census Geocoder API
def get_census_tract(street, city, state):
    url = (f"https://geocoding.geo.census.gov/geocoder/geographies/address"
           f"?street={requests.utils.quote(street)}"
           f"&city={requests.utils.quote(city)}" 
           f"&state={requests.utils.quote(state)}"
           f"&benchmark=Public_AR_Census2020"
           f"&vintage=Census2020_Census2020"
           f"&layers=10"
           f"&format=json")

    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return "Error in API call"

# Extract GEOID and BLOCK from the response
def extract_geoid_block(data):
    try:
        census_block = data['result']['addressMatches'][0]['geographies']['Census Blocks'][0]
        geoid = census_block['GEOID']
        block = census_block['BLOCK']
        return geoid, block
    except (IndexError, KeyError):
        return None, None

# Read in CSV 
df = pd.read_csv('https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_HB550_ECT.csv')

# Streamlit app
def main():
    st.title("Census Tract Finder")

    # Get user inputs
    street = st.text_input("Street", "1800 Washington Bvld")
    city = st.text_input("City", "Baltimore") 
    state = st.text_input("State", "MD")

    if st.button("Find Census Tract"):
        data = get_census_tract(street, city, state)
        geoid, block = extract_geoid_block(data)

        # Display GEOID and BLOCK if they were found
        if geoid and block:
            st.write(f"GEOID: {geoid}")
            st.write(f"BLOCK: {block}")

        # Check eligibility based on GEOID
        if geoid in df['GEOID'].values:
            st.write("This is an eligible location based on MD HB 550") 
        else:
            st.write("This is NOT an eligible location based on MD HB 550")
            
if __name__ == "__main__":
    main()
