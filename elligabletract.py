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
        st.error("Error in API call")
        return None

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
        st.error("Could not extract details from the response")
        return None, None, None, None, None

# Function to display a map with a given point and a GeoJSON layer
def display_map(latitude, longitude, geojson_url):
    # Define a layer to display the point
    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"position": [longitude, latitude], "color": [255, 0, 0], "radius": 100}],
        get_position="position",
        get_color="color",
        get_radius="radius",
    )

    # Define a layer for the GeoJSON
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_url,
        opacity=0.5,
        stroked=False,
        filled=True,
        extruded=True,
    )

    # Set the view state for the map
    view_state = pdk.ViewState(latitude=latitude, longitude=longitude, zoom=12)

    # Render the map with both layers
    st.pydeck_chart(pdk.Deck(layers=[point_layer, geojson_layer], initial_view_state=view_state))

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
        if data:
            geoid, block, zip_code, x, y = extract_details(data)
            # Display GEOID, BLOCK, and ZIP if they were found
            if geoid and block:
                st.write(f"GEOID: {geoid}")
                st.write(f"BLOCK: {block}")
                st.write(f"ZIP Code: {zip_code}")

            # Check eligibility based on GEOID
            if geoid and geoid in df['GEOID'].values:
                st.success("This is an eligible location based on MD HB 550") 
            else:
                st.error("This is NOT an eligible location based on MD HB 550")

            # Display the map with the found coordinates and the GeoJSON layer
            if y and x:
                # URL to the GeoJSON data on GitHub (replace with your actual URL)
                geojson_url = 'https://raw.githubusercontent.com/rmkenv/censusgeocode/main/Maryland_Education_Facilities_-_PreK_thru_12_Education_(Public_Schools).geojson'
                display_map(y, x, geojson_url)

if __name__ == "__main__":
    main()
