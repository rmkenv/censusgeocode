import streamlit as st
import requests
import pandas as pd

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
        data = response.json()
        return data
    else:
        return "Error in API call"

# Streamlit app layout
def main():
    st.title("Census Tract Finder")

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
                geoid = census_block['GEOID']
                block = census_block['BLOCK']
                blkgrp = census_block['BLKGRP']
                
                # Display the information in a table
                st.write("Matched Address Information:")
                info_table = pd.DataFrame({
                    'GEOID': [geoid],
                    'Block': [block],
                    'Block Group': [blkgrp]
                })
                st.table(info_table)
            except (KeyError, IndexError):
                st.error("Could not extract the details from the response.")
        else:
            st.error(result)

if __name__ == "__main__":
    main()
