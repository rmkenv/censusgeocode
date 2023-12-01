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

# Function to fetch school data
def fetch_school_data():
    school_url = 'https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_k12_to_20ACStract.geojson'
    response = requests.get(school_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to load school data.")
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

    # Load HB550 and school data
    hb550_data = fetch_hb550_data()
    school_data = fetch_school_data()

    # Address inputs
    street = st.text_input("Street", "100 State Circle")
    city = st.text_input("City", "Annapolis")
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
                st.markdown("---")  # Thick horizontal line
                st.subheader("MD HB550 Information")  # Subheader for HB550
                # Add a link to a PDF
                pdf_url = "https://mgaleg.maryland.gov/2023RS/chapters_noln/Ch_98_hb0550T.pdf"
                st.markdown(f"[Review MD HB550:https://mgaleg.maryland.gov/2023RS/chapters_noln/Ch_98_hb0550T.pdf]({pdf_url})", unsafe_allow_html=True)
                hb550_match = next((item for item in hb550_data if item['GEOID'] == geoid), None)
                
                if hb550_match:
                    st.success("This location is in an area listed in HB 550.") 
                    # Display the HB550 information in a table
                    hb550_info_table = pd.DataFrame([hb550_match])
                    st.table(hb550_info_table)
                else:
                    st.error("This location is NOT in an area listed in HB 550.")
                    
                # Find and display schools information
                st.markdown("---")  # Thick horizontal line
                st.subheader("Schools Information")
                st.write ("Please refer to the specific Program FOA to determine if this information is needed.")
                with st.expander("Schools Results"):
                # Adding normal text note under header for schools 
                    st.write("This section shows information about schools associated with your address search. "
                             "Note that some listed schools may not be physically located in an eligible census tract. "
                             "However, they may enroll students who reside in qualifying tracts. "
                             "Please contact MEA if you need help determining your eligibility based on school attendance boundaries.")
                    schools_matched = [feature['properties'] for feature in school_data['features']
                                   if feature['properties']['GEOID20'] == geoid]
                    if schools_matched:
                        schools_info_table = pd.DataFrame(schools_matched)
                        st.table(schools_info_table)
                    else:
                        st.info("No schools found for this Census Tract.")
                    
            except (KeyError, IndexError):
                st.error("Could not extract the details from the response.")
        else:
            st.error(result)

if __name__ == "__main__":
    main()
