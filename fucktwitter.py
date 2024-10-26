import requests
import json
import argparse
import logging
import os
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Configuration
ACCESS_TOKEN = 'your_access_token'  # Replace with your valid access token
BASE_URL = 'https://api.x.com/v1/users/'  # Replace with the actual endpoint

def download_profile_data(username, output_format='json'):
    url = f'{BASE_URL}{username}/data'  # Adjust based on actual API documentation
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Accept': 'application/json',
        'User-Agent': 'CustomXProfileDownloader/1.0',  # Custom User-Agent
    }

    try:
        logger.info(f'Starting data download for user: {username}')
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        data = response.json()
        generated_on = datetime.now().strftime("%B %d, %Y")
        expires_on = (datetime.now() + timedelta(days=7)).strftime("%B %d, %Y")
        estimated_size = f"{len(json.dumps(data)) // 1024} KB"

        # Log the metadata
        logger.info(f"X data (1 of 1)")
        logger.info(f"Generated on: {generated_on}")
        logger.info(f"Expires on: {expires_on}")
        logger.info(f"Estimated size: {estimated_size}")

        # Save the data to a file
        file_name = f"{username}_profile_data.{output_format}"
        if output_format == 'json':
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
        elif output_format == 'txt':
            with open(file_name, 'w') as f:
                for key, value in data.items():
                    f.write(f"{key}: {value}\n")
        else:
            logger.error("Unsupported output format. Please use 'json' or 'txt'.")
            return

        logger.info(f"Profile data downloaded successfully: {file_name}")

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred for {username}: {http_err}")  # Log HTTP errors
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred for {username}: {req_err}")  # Log request errors
    except Exception as e:
        logger.error(f"An error occurred for {username}: {e}")  # Log any other exceptions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download X.com profile data for a specified username.')
    parser.add_argument('username', type=str, help='The username of the profile to download data for')
    parser.add_argument('--output', type=str, choices=['json', 'txt'], default='json', help='Output format (json or txt)')

    args = parser.parse_args()
    
    download_profile_data(args.username, args.output)
