import requests
import json

# Replace with your NOAA API Token
API_TOKEN = 'aLGTWgEGFuUeITvEvtloguCXEQVmWGum'

# Base URL for the locations endpoint
BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations"

# Headers for the request
headers = {"Token": API_TOKEN}

# Parameters for the request
params = {
    "limit": 1000,  # Number of results per page
    "offset": 1     # Starting index
}

# Pagination loop to fetch and save data
file_counter = 1
while True:
    params["offset"] = (file_counter - 1) * params["limit"] + 1
    print(f"Fetching records for file {file_counter}...")

    # Send the GET request
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        break

    # Parse the response
    data = response.json()

    # Save each response to a separate JSON file
    filename = f"locations_{file_counter}.json"
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to '{filename}'.")

    # Check if more data exists
    total_count = data["metadata"]["resultset"]["count"]
    if file_counter * params["limit"] >= total_count:
        break

    # Increment file counter for the next request
    file_counter += 1

print("All data fetched and saved.")
