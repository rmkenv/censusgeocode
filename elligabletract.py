import streamlit as st
import pandas as pd
import requests

# Replace with the actual URL of your CSV file
CSV_URL = 'https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_HB550_ECT'

# GEOID column name
GEOID_COLUMN_NAME = 'GEOID'

# New caching mechanism as per Streamlit's update
@st.experimental_memo
def get_eligible_geoids():
    df = pd.read_excel(CSV_URL)
    eligible_geoids = df[GEOID_COLUMN_NAME].astype(str).tolist()
    return eligible_geoids

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

# Streamlit app layout
def main():
    st.title("Census Tract Finder")

    # Address inputs
    street = st.text_input("Street", "4600 Silver Hill Rd")
    city = st.text_input("City", "Washington")
    state = st.text_input("State", "DC")

    # Load eligible GEOIDs
    eligible_geoids = get_eligible_geoids()

    if st.button("Find Census Tract"):
        response_data = get_census_tract(street, city, state)
        if isinstance(response_data, dict):
            # Show the full JSON response collapsed
            st.expander("Full JSON Response", expanded=False).json(response_data)

            # Extract and display GEOID and BLOCK
            geoid, block = extract_geoid_block(response_data)
            if geoid and block:
                st.write(f"GEOID: {geoid}")
                st.write(f"BLOCK: {block}")
                # Check if the location is eligible
                if geoid in eligible_geoids:
                    st.success("This location is an eligible location under MD HB 550.")
                else:
                    st.error("This location is not eligible under MD HB 550.")
            else:
                st.write("GEOID and BLOCK could not be extracted.")
        else:
            st.write(response_data)

if __name__ == "__main__":
    main()
