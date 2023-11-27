# Census Tract Finder

## Overview
The Census Tract Finder is a Streamlit web application designed to help users find census tract information for a given address. It uses the Census Geocoder API to locate census tracts and compares the results with HB550 data.

## Features
- Input fields for street, city, and state to find the corresponding census tract.
- JSON response view for the API call.
- Display of GEOID, Block, and Block Group from the census data.
- Matching with HB550 data and displaying relevant information if a match is found.
- User-friendly error handling for API issues or data mismatches.

## How to Use
1. Enter the street, city, and state for the address you wish to find the census tract for.
2. Click the "Find Census Tract" button to retrieve and display the information.
3. If the address matches an area listed in HB 550, additional information will be displayed.

## Data Sources
- Census Geocoder API: Used to retrieve census tract information based on the provided address.
- HB550 Data: A JSON file hosted on GitHub, containing areas related to HB550 legislation.

## Setup and Installation
To run this application on your local machine, you'll need to have Python installed along with the following libraries:
- Streamlit
- Requests
- Pandas

## Contributions
Contributions to the Census Tract Finder are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any queries or feedback regarding the Census Tract Finder, please open an issue in the GitHub repository.

## Acknowledgments
- Thanks to the contributors of the Census Geocoder API for providing access to the data.
- Appreciation to the maintainers of the HB550 data set (https://energy.maryland.gov/SiteAssets/Pages/CensusTractsRPS/110723%20MD%20HB%20550%20Eligible%20Census%20Tracts%20Full%20List.pdf) for making the information publicly available.


## Clone the repository, navigate to the app's directory, and run:
```bash
streamlit run elligabletracts.py


## Contributions
Contributions to the Census Tract Finder are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any queries or feedback regarding the Census Tract Finder, please open an issue in the GitHub repository.

## Acknowledgments
- Thanks to the contributors of the Census Geocoder API for providing access to the data.
- Appreciation to the maintainers of the HB550 data set (https://energy.maryland.gov/SiteAssets/Pages/CensusTractsRPS/110723%20MD%20HB%20550%20Eligible%20Census%20Tracts%20Full%20List.pdf) for making the information publicly available.



