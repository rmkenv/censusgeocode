import streamlit as st
import pandas as pd
import requests

# Function to get census tract using Census Geocoder API
def get_census_tract(street, city, state):
    # ... (No changes in this function)

# Extract GEOID, BLOCK, ZIP, tract, and coordinates from the response
def extract_details(data):
    try:
        address_match = data['result']['addressMatches'][0]
        census_block = address_match['geographies']['Census Blocks'][0]
        geoid = census_block['GEOID']
        block = census_block['BLOCK']
        tract = census_block['TRACT']
        zip_code = address_match['addressComponents']['zip']
        coordinates = address_match['coordinates']
        x = coordinates['x']
        y = coordinates['y']
        return geoid, block, tract, zip_code, x, y
    except (IndexError, KeyError):
        return None, None, None, None, None, None

# Read in CSV for eligibility based on GEOID and to get the Census Tract and County Name
hb550_df = pd.read_csv('https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_HB550_ECT.csv')

# Function to get Census Tract and County Name from GEOID
def get_tract_info(geoid, tract):
    tract_info = hb550_df[hb550_df['GEOID'] == geoid]
    if not tract_info.empty:
        tract_name = tract_info.iloc[0]['Census Tract']
        county_name = tract_info.iloc[0]['County Name']
        return tract_name, county_name
    else:
        return "Tract not found", "County not found"

# Streamlit app
def main():
    st.title("Census Tract Finder")

    # Get user inputs
    street = st.text_input("Street", "1800 Washington Bvld")
    city = st.text_input("City", "Baltimore")
    state = st.text_input("State", "MD")

    if st.button("Find Census Tract"):
        data = get_census_tract(street, city, state)
        geoid, block, tract, zip_code, x, y = extract_details(data)
        tract_name, county_name = get_tract_info(geoid, tract)

        # Display GEOID, BLOCK, TRACT, COUNTY NAME, ZIP, and coordinates if they were found
        if geoid and block:
            st.write(f"GEOID: {geoid}")
            st.write(f"BLOCK: {block}")
            st.write(f"CENSUS TRACT: {tract_name}")
            st.write(f"COUNTY NAME: {county_name}")
            st.write(f"ZIP Code: {zip_code}")
            st.write(f"Coordinates: (Latitude: {y}, Longitude: {x})")

        # Check eligibility based on GEOID
        if geoid and geoid in hb550_df['GEOID'].values:
            st.write("This location is eligible based on MD HB 550")
        else:
            st.write("This location is NOT eligible based on MD HB 550")

if __name__ == "__main__":
    main()
