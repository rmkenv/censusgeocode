import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

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

# Extract GEOID, BLOCK, ZIP, and coordinates from the response
def extract_details(data):
    try:
        address_match = data['result']['addressMatches'][0]
        census_block = address_match['geographies']['Census Blocks'][0]
        geoid = census_block['GEOID']
        block = census_block['BLOCK']
        zip_code = address_match['addressComponents']['zip']
        coordinates = address_match['coordinates']
        x = coordinates['x']
        y = coordinates['y']
        return geoid, block, zip_code, x, y
    except (IndexError, KeyError):
        return None, None, None, None, None

# Function to create a map with a GeoJSON layer
def create_map(latitude, longitude, geojson_url):
    # Define a layer to display on the map
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_url,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
    )
    
    # Set the viewport location
    view_state = pdk.ViewState(latitude=latitude, longitude=longitude, zoom=11, bearing=0, pitch=0)

    # Render the map
    st.pydeck_chart(pdk.Deck(layers=[geojson_layer], initial_view_state=view_state))

# Read in CSV 
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
        geoid, block, zip_code, x, y = extract_details(data)

        # Display GEOID, BLOCK, ZIP, and coordinates if they were found
        if geoid and block:
            st.write(f"GEOID: {geoid}")
            st.write(f"BLOCK: {block}")
            st.write(f"ZIP Code: {zip_code}")
            st.write(f"Coordinates: (Latitude: {y}, Longitude: {x})")  # Display coordinates

        # Check eligibility based on GEOID
        if geoid and geoid in df['GEOID'].values:
            st.write("This is an eligible location based on MD HB 550") 
        else:
            st.write("This is NOT an eligible location based on MD HB 550")
        
        # Create and display the map if coordinates are found
        if y and x:
            # URL to the GeoJSON data on GitHub (replace with your actual URL)
            geojson_url = 'https://raw.githubusercontent.com/rmkenv/censusgeocode/main/Maryland_Education_Facilities_-_PreK_thru_12_Education_(Public_Schools).geojson'
            create_map(y, x, geojson_url)

if __name__ == "__main__":
    main()
