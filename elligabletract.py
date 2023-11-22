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
    tract_info = hb550_df[hb550_df['GEOID'].astype(str).str.contains(tract)]
    if not tract_info.empty:
        tract_name = tract_info.iloc[0]['Census Tract']
        county_name = tract_info.iloc[0]['County Name']
        return tract_name, county_name
    else:
        return "Tract not found", "County not found"

# Streamlit app
def main():
    st.title("Census Tract Finder")
 # Additional information link
    st.markdown(
        "For additional information on MD HB 550 please visit "
        "[MD HB 550 Information](https://mgaleg.maryland.gov/2023RS/chapters_noln/Ch_98_hb0550T.pdf)"
    )
    # Get user inputs
    street = st.text_input("Street", "1800 Washington Bvld")
    city = st.text_input("City", "Baltimore")
    state = st.text_input("State", "MD")

    if st.button("Find Census Tract"):
        data = get_census_tract(street, city, state)
        geoid, block, tract, zip_code, x, y = extract_details(data)
        tract_name, county_name = get_tract_info(geoid, tract)

        # Display GEOID, BLOCK, CENSUS TRACT, COUNTY NAME, ZIP, and coordinates if they were found
        if geoid and block:
            st.write(f"GEOID: {geoid}")
            st.write(f"BLOCK: {block}")
            st.write(f"CENSUS TRACT: {tract_name}")
            st.write(f"COUNTY NAME: {county_name}")
            st.write(f"ZIP Code: {zip_code}")
            st.write(f"Coordinates: (Latitude: {y}, Longitude: {x})")

        # Check eligibility based on GEOID
if geoid and geoid in hb550_df['GEOID'].values:
    st.markdown(
        f"<h3>This location <b>is eligible</b> based on "
        f"[MD HB 550](https://mgaleg.maryland.gov/2023RS/chapters_noln/Ch_98_hb0550T.pdf)</h3>", 
        unsafe_allow_html=True)
else:
    st.markdown(
        f"<h3>This location <b><u>is NOT eligible</u></b> based on "
        f"[MD HB 550](https://mgaleg.maryland.gov/2023RS/chapters_noln/Ch_98_hb0550T.pdf)</h3>", 
        unsafe_allow_html=True)

if __name__ == "__main__":
    main()
