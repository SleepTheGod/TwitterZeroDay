import requests
import json
import os
from datetime import datetime, timedelta
import argparse

# Configuration
ACCESS_TOKEN = 'your_access_token'  # Replace with your access token
BASE_URL = 'https://api.x.com/v1/users/'  # Replace with the actual endpoint

def download_profile_data(username):
    url = f'{BASE_URL}{username}/data'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Accept': 'application/json',
    }
    
    response = requests.get(url, headers=headers)
    
    # Handle the response
    if response.status_code == 200:
        data = response.json()
        generated_on = datetime.now().strftime("%B %d, %Y")
        expires_on = (datetime.now() + timedelta(days=7)).strftime("%B %d, %Y")
        estimated_size = f"{len(json.dumps(data)) // 1024} KB"

        # Output the details
        print(f"X data (1 of 1)")
        print(f"Generated on: {generated_on}")
        print(f"Expires on: {expires_on}")
        print(f"Estimated size: {estimated_size}")

        # Save the data to a file
        file_name = f"{username}_profile_data.json"
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Profile data downloaded successfully: {file_name}")
    elif response.status_code == 404:
        print(f"User '{username}' not found.")
    elif response.status_code == 403:
        print("Access denied. Please check your access token.")
    else:
        print(f"Failed to download profile data for {username}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download X.com profile data for a specified username.')
    parser.add_argument('username', type=str, help='The username of the profile to download data for')
    
    args = parser.parse_args()
    
    download_profile_data(args.username)
