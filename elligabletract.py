import streamlit as st
import pandas as pd
import requests

# Load data 
@st.cache_data
def load_data():
  url = 'https://raw.githubusercontent.com/user/repo/census.csv'
  df = pd.read_csv(url)
  return df

df = load_data()

# Get eligible GEOIDs
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

  try:
    response = requests.get(url, params=params)
    data = response.json()

    if 'result' not in data:
      raise Exception("No result in response")

    result = data['result']

    if 'addressMatches' not in result:
      raise Exception("No address matches found")

    address_match = result['addressMatches'][0]

    if 'geographies' not in address_match:
      raise Exception("No geographies found")

    geo = address_match['geographies']

    census_tract = geo['Census Blocks'][0]['GEOID']
    census_block = geo['Census Blocks'][0]['BLOCK']

    return census_tract, census_block
  
  except Exception as e:
    st.error(f"Error: {e}")
    return None, None

# Streamlit app
st.title('Census Tract Finder') 

street = st.text_input('Street')
city = st.text_input('City')  
state = st.text_input('State')

if st.button('Find Census Tract'):

  census_tract, census_block = get_census_data(street, city, state)

  if census_tract:
    st.write(f"Census Tract: {census_tract}")
    st.write(f"Census Block: {census_block}")

    if census_tract in eligible_geoids:
      st.success("Location is eligible")
    else:
      st.error("Location is not eligible")

  else:
    st.error("Could not find census data for location")
