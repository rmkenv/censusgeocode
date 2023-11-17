import streamlit as st
import requests
import pandas as pd

# Assuming you've uploaded the CSV file on GitHub and have its raw URL
CSV_URL = 'https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_HB550_ECT'

# Function to fetch and read the CSV from GitHub
@st.cache
def get_eligible_geoids():
    # Fetch the CSV file from the GitHub raw URL
    df = pd.read_csv(CSV_URL)
    # Assuming the GEOID/Census Tract Identifier is in the 'GEOID' column
    eligible_geoids = df['GEOID'].astype(str).tolist()
    return eligible_geoids

# Modify your existing Streamlit app layout function
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
