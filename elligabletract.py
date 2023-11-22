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

# Load the county FIPS to name mapping
county_fips_df = pd.read_csv('https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_County_FIPS.csv')

# Function to get county name from county FIPS code
def get_county_name(county_fips):
    county_row = county_fips_df[county_fips_df['County_FIPS'] == county_fips]
    if not county_row.empty:
        return county_row.iloc[0]['County_Name']
    else:
        return "County not found"

# Extract GEOID, BLOCK, ZIP, county FIPS, and coordinates from the response
def extract_details(data):
    try:
        address_match = data['result']['addressMatches'][0]
        census_block = address_match['geographies']['Census Blocks'][0]
        geoid = census_block['GEOID']
        block = census_block['BLOCK']
        county_fips = census_block['COUNTY']
        county_name = get_county_name(county_fips)
        zip_code = address_match['addressComponents']['zip']
        coordinates = address_match['coordinates']
        x = coordinates['x']
        y = coordinates['y']
        return geoid, block, county_fips, county_name, zip_code, x, y
    except (IndexError, KeyError):
        return None, None, None, None, None, None, None

# Read in CSV for eligibility based on GEOID
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
        geoid, block, county_fips, county_name, zip_code, x, y = extract_details(data)

        # Display GEOID, BLOCK, COUNTY FIPS, COUNTY NAME, ZIP, and coordinates if they were found
        if geoid and block:
            st.write(f"GEOID: {geoid}")
            st.write(f"BLOCK: {block}")
            st.write(f"COUNTY FIPS: {county_fips}")
            st.write(f"COUNTY NAME: {county_name}")
            st.write(f"ZIP Code: {zip_code}")
            st.write(f"Coordinates: (Latitude: {y}, Longitude: {x})")

        # Check eligibility based on GEOID
        if geoid and geoid in df['GEOID'].values:
            st.write("This location is eligible based on MD HB 550")
        else:
            st.write("This location is NOT eligible based on MD HB 550")

if __name__ == "__main__":
    main()
