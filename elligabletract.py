import streamlit as st
import pandas as pd
import requests

# Function to get census tract  
def get_census_tract(street, city, state):
  # API request
  
# Extract GEOID and BLOCK
def extract_geoid_block(data):
  # Extract GEOID and BLOCK

df = pd.read_csv('https://raw.githubusercontent.com/rmkenv/censusgeocode/main/MD_HB550_ECT.csv')

def main():

  st.title("Census Tract Finder")

  street = st.text_input("Street")
  city = st.text_input("City")
  state = st.text_input("State")

  if st.button("Find"):

    data = get_census_tract(street, city, state)

    geoid, block = extract_geoid_block(data)
    zip_code = data['result']['addressMatches'][0]['addressComponents']['zip']

    st.write(f"GEOID: {geoid}")
    st.write(f"BLOCK: {block}")
    st.write(f"ZIP Code: {zip_code}")

    if geoid in df['GEOID'].values:
      st.write("This is an eligible location based on MD HB 550")
    else:
      st.write("This is NOT an eligible location based on MD HB 550")

if __name__ == "__main__":
  main()
