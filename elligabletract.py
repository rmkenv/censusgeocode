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
            st.write(f"Coordinates: ({y}, {x})")  # Display coordinates (Latitude, Longitude)

        # Check eligibility based on GEOID
        if geoid in df['GEOID'].values:
            st.write("This is an eligible location based on MD HB 550") 
        else:
            st.write("This is NOT an eligible location based on MD HB 550")

if __name__ == "__main__":
    main()
