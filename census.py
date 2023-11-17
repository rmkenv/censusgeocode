import streamlit as st
import requests

# Function to get census tract using Census Geocoder API
def get_census_tract(street, city, state):
    # Construct the API request URL
    url = (f"https://geocoding.geo.census.gov/geocoder/geographies/address"
           f"?street={requests.utils.quote(street)}"
           f"&city={requests.utils.quote(city)}"
           f"&state={requests.utils.quote(state)}"
           f"&benchmark=Public_AR_Current"
           f"&vintage=Census2020_Census2020"
           f"&layers=10"
           f"&format=json")

    # Make the API request
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            # Extracting the geography information
            geographies = data['result']['geographies']['Census Blocks']
            return geographies
        except (IndexError, KeyError):
            return "No match found or invalid response format"
    else:
        return "Error in API call"

# Streamlit app layout
def main():
    st.title("Census Tract Finder")

    # Address inputs
    street = st.text_input("Street", "4600 Silver Hill Rd")
    city = st.text_input("City", "Washington")
    state = st.text_input("State", "DC")

    if st.button("Find Census Tract"):
        result = get_census_tract(street, city, state)
        if isinstance(result, list):
            st.json(result)
        else:
            st.write(result)

if __name__ == "__main__":
    main()
