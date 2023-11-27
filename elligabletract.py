import streamlit as st
import requests
import pandas as pd

# Function to fetch HB550 data
def fetch_hb550_data():
    hb550_url = 'https://raw.githubusercontent.com/rmkenv/censusgeocode/main/HB505.json'
    response = requests.get(hb550_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to load HB550 data.")
        return []

# Function to get census tract using Census Geocoder API
def get_census_tract(street, city, state):
    # Construct the API request URL
    url = (f"https://geocoding.geo.census.gov/geocoder/geographies/address"
           f"?street={requests.utils.quote(street)}"
           f"&city={requests.utils.quote(city)}"
           f"&state={requests.utils.quote(state)}"
           f"&benchmark=Public_AR_Census2020"
           f"&vintage=Census2020_Census2020"
           f"&layers=10"
           f"&format=json")
    # Make the API request
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return "Error in API call"

# Streamlit app layout
def main():
    st.title("Census Tract Finder")

    # Load HB550 data
    hb550_data = fetch_hb550_data()

    # Address inputs
    street = st.text_input("Street", "1400 Washington Bvld")
    city = st.text_input("City", "Baltimore")
    state = st.text_input("State", "MD")

    if st.button("Find Census Tract"):
        result = get_census_tract(street, city, state)
        if isinstance(result, dict):
            with st.expander("Show JSON Response", expanded=False):
                st.json(result)
            
            # Extracting the required information
            try:
                address_matches = result['result']['addressMatches'][0]
                census_block = address_matches['geographies']['Census Blocks'][0]
                geoid_full = census_block['GEOID']
                geoid = geoid_full[:-4]
                block = census_block['BLOCK']
                blkgrp = census_block['BLKGRP']
                
                # Display the matched address information
                st.write("Matched Address Information:")
                info_table = pd.DataFrame({
                    'GEOID': [geoid],
                    'Block': [block],
                    'Block Group': [blkgrp]
                })
                st.table(info_table)
                
                # Check if the GEOID is in the HB550 data and display relevant information
                st.markdown("---")  # Horizontal line
                st.header("HB550 Information")
                hb550_match = next((item for item in hb550_data if item['GEOID'] == geoid), None)
                
                if hb550_match:
                    st.success("This location is in an area listed in HB 550.") 
                    # Display the HB550 information in a table
                    hb550_info_table = pd.DataFrame([hb550_match])
                    st.table(hb550_info_table)
                else:
                    st.error("This location is NOT in an area listed in HB 550.")
                    
            except (KeyError, IndexError):
                st.error("Could not extract the details from the response.")
        else:
            st.error(result)

if __name__ == "__main__":
    main()
