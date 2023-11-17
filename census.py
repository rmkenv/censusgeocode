import streamlit as st
import requests

# Function to get census tract using Census Geocoder API
def get_census_tract(address):
    url = f'https://geocoding.geo.census.gov/geocoder/geographies/address?street={address}&benchmark=Public_AR_Census2020&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            # Extracting the GeoID and Census Tract Name
            result = data['result']['addressMatches'][0]['geographies']['Census Tracts'][0]
            geoid = result['GEOID']
            name = result['NAME']
            return geoid, name
        except IndexError:
            return "No match found", "No match found"
    else:
        return "Error in API call", "Error in API call"

# Streamlit app layout
def main():
    st.title("Census Tract Finder")
    
    # Address input
    address = st.text_input("Enter the address:", "1800 Washington Blvd, Baltimore, MD, 21230")
    
    if st.button("Find Census Tract"):
        geoid, name = get_census_tract(address)
        st.write(f"GeoID: {geoid}")
        st.write(f"Census Tract Name: {name}")

if __name__ == "__main__":
    main()
