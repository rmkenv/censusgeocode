import streamlit as st
import pandas as pd 
import requests

# Load data from GitHub URL 
@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_HB550_ECT'
    df = pd.read_csv(url)
    return df

df = load_data() 

# Extract eligible GEOIDs
eligible_geoids = df['GEOID'].astype(str).tolist()

# Census API function 
def get_census_data(street, city, state):
    url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    params = {
        "address": f"{street}, {city}, {state}", 
        "benchmark": "Public_AR_Census2020",
        "vintage": "Census2020_Census2020", 
        "layers": "10",
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    
    if response.ok:
        data = response.json()
        return data['result']['geographies']
    else:
        return None

# Streamlit UI
st.title("Census Tract Finder")

street = st.text_input("Street")  
city = st.text_input("City")
state = st.text_input("State")

if st.button("Find Census Tract"):

    data = get_census_data(street, city, state)
    
    if data:
        census_tract = data['Census Tracts'][0]['GEOID']
        census_block = data['Census Blocks'][0]['GEOID']
        
        st.write(f"Census Tract: {census_tract}")
        st.write(f"Census Block: {census_block}")
        
        if census_tract in eligible_geoids:
            st.success("Location is eligible")
        else:
            st.error("Location is not eligible")
            
    else:
        st.error("Error getting census data")
