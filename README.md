# Census Tract Finder - GitHub README

## Overview

This repository contains code for a simple web application that utilizes the Census Geocoder API to find census tract information based on a street address. It's built using Streamlit for the web interface, Pandas for data manipulation, and the `requests` library for API calls.

## Features

- **Census Tract Lookup**: Enter a street address to retrieve the census tract, block number, zip code, and geographical coordinates.
- **Eligibility Check**: Compares the GEOID from the census data to a predefined list to determine eligibility for specific criteria based on MD HB 550.
- **Error Handling**: Provides error messages if the API call is unsuccessful.

## Installation

1. Clone this repository.
2. Install the requirements using `pip install -r requirements.txt` (assuming you have `pip` and Python already installed).

## Usage

To run the web application:

1. Execute `streamlit run app.py` in the terminal (assuming `app.py` is the filename of the script).
2. The web interface should open in your default browser.
3. Input the street, city, and state to get the census information and eligibility status.

## How It Works

- **API Call**: The `get_census_tract` function constructs a URL to query the Census Geocoder API and returns the JSON response.
- **Data Extraction**: The `extract_details` function parses the JSON response to extract relevant details like the GEOID, block number, etc.
- **CSV Data**: Reads a CSV file containing census tract data relevant to MD HB 550 for eligibility checking.
- **Streamlit Interface**: The `main` function creates a user-friendly interface to input address data and view results.

## Streamlit App Flow

1. The user enters a street address.
2. Upon clicking "Find Census Tract", the app calls the Census Geocoder API.
3. If successful, it displays the GEOID, block number, County, zip code, and coordinates.
4. It then checks if the GEOID matches an eligible location according to MD HB 550 and informs the user accordingly.

## Notes

- Ensure that you have an internet connection to fetch data from the Census Geocoder API.
- The CSV file for MD HB 550 eligibility is currently loaded from a remote URL.

Feel free to fork, modify, and use this code as per your needs. If you encounter any issues, please open an issue in this repository.
