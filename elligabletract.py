import streamlit as st
import requests

# Hardcoded data dictionary
data_dict = [
    {'GEOID': '24001000100', 'Census Tract': '1', 'County Name': 'Allegany County'},
    {'GEOID': '24001000200', 'Census Tract': '2', 'County Name': 'Allegany County'},
    {'GEOID': '24001000500', 'Census Tract': '5', 'County Name': 'Allegany County'},
    {'GEOID': '24001000600', 'Census Tract': '6', 'County Name': 'Allegany County'},
    {'GEOID': '24001000700', 'Census Tract': '7', 'County Name': 'Allegany County'}
]

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

# Function to get Census Tract and County Name from GEOID
def get_tract_info(geoid):
    for item in data_dict:
        if item['GEOID'] == geoid:
            return item['Census Tract'], item['County Name']
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
        if data != "Error in API call":
            geoid, block, tract, zip_code, x, y = extract_details(data)
            if geoid:
                tract_name, county_name = get_tract_info(geoid)

                # Display GEOID, BLOCK, CENSUS TRACT, COUNTY NAME, ZIP, and coordinates if they were found
                st.write(f"GEOID: {geoid}")
                st.write(f"BLOCK: {block}")
                st.write(f"CENSUS TRACT: {tract_name}")
                st.write(f"COUNTY NAME: {county_name}")
                st.write(f"ZIP Code: {zip_code}")
                st.write(f"Coordinates: (Latitude: {y}, Longitude: {x})")

                # Check eligibility based on GEOID
                if geoid in (item['GEOID'] for item in data_dict):
                    st.write("This location is eligible based on MD HB 550")
                else:
                    st.write("This location is NOT eligible based on MD HB 550")
            else:
                st.write("No GEOID found for the provided address.")
        else:
            st.write("An error occurred while calling the Census Geocoder API.")

if __name__ == "__main__":
    main()
