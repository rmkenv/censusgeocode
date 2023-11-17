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

# Display a map with GeoJSON points
def display_map(geojson_data):
    # Define initial view state
    view_state = pdk.ViewState(
        latitude=38.806352,  # Center of Maryland Latitude
        longitude=-77.268416,  # Center of Maryland Longitude
        zoom=7,
        pitch=0,
        bearing=0
    )

    # Layer for the GeoJSON data
    schools_layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_data,
        get_fill_color=[0, 0, 255, 160],  # Set the fill color to blue
        pickable=True,  # Allow each feature to be clickable
        auto_highlight=True,  # Automatically highlight the feature on hover
        tooltip="SCHOOL_NAME"  # Set the tooltip to the school name
    )

    # Render the map with the schools layer
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[schools_layer]
    ))

# Streamlit app
def main():
    st.title("Maryland Education Facilities - PreK thru 12")

    # GeoJSON data for schools in Maryland
    geojson_data = {
        "type": "FeatureCollection",
        # ... [Include the rest of the GeoJSON data here] ...
    }

    # Button to display schools on map
    if st.button("Display Schools on Map"):
        display_map(geojson_data)

if __name__ == "__main__":
    main()
