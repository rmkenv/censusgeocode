import streamlit as st
import requests

# Function to get census tract using Census Geocoder API
def get_census_tract(address):
    # Format the address for URL encoding
    formatted_address = requests.utils.quote(address)
    
    # Construct the API request URL
    url = (f"https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
           f"?address={formatted_address}&benchmark=Public_AR_Current&format=json")

    # Make the API request
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            # Extracting the address match
            result = data['result']['addressMatches'][0]
            return result
        except IndexError:
            return "No match found"
    else:
        return "Error in API call"

# Streamlit app layout
def main():
    st.title("Census Tract Finder")
    
    # Address input
    address = st.text_input("Enter the address:", "4600 Silver Hill Rd, Washington, DC 20233")
    
    if st.button("Find Census Tract"):
        result = get_census_tract(address)
        if isinstance(result, dict):
            st.json(result)
        else:
            st.write(result)

if __name__ == "__main__":
    main()
