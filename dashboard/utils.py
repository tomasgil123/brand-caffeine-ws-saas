import re
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import streamlit as st
import base64
import json
from google.cloud import storage
from io import StringIO
from google.api_core.exceptions import NotFound
import requests


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def is_cookie_expired(cookie_string):
    # Regular expression to find the number after &expire=
    match = re.search(r'&expire=(\d+)', cookie_string)

    if match:
        expire_timestamp = int(match.group(1))
        current_timestamp = int(datetime.now().timestamp() * 1000)
        
        if current_timestamp > expire_timestamp:
            return True
        else:
            return False
    else:
        return True

def get_brand_token(brand_name, cookie):
    endpoint = "https://www.faire.com/api/v2/search/suggestions"

    print(f"Searching for brand: {brand_name}")

    default_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': default_user_agent,
        'Cookie': cookie
    }

    payload = {
        "query": f"{brand_name}"
    }

    try:
        # Make the GET request to the API
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                suggested_brands = data.get("suggested_brands", [])
                if len(suggested_brands) > 0:
                    brand_token = suggested_brands[0].get('token', None)
                    return brand_token
                else:
                    print("No brand found")
                    return None
        else:
            print(f"An error occurred, status code not 200: {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def get_user_from_cookie(cookie_string):
    """Extracts the user from the cookie."""
    match = re.search(r'indigofair_session=([^;]+)', cookie_string)

    if match:
        jwt_token = match.group(1)
        payload = jwt_token.split('.')[1]
        decoded_payload = base64.b64decode(payload + '=' * (-len(payload) % 4)).decode('utf-8')
        user_info = json.loads(decoded_payload)
        st.write(user_info)
    else:
        st.error("Invalid cookie")

creds_dict = {
        "type": "service_account",
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }

def get_data_from_google_spreadsheet(spreadsheet_id, range_name):

    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Use the Sheets API to get the data
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    # Check if data was retrieved successfully
    if not values:
        return pd.DataFrame()
    else:
        # Create a DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])
        return df

def download_csv_from_cloud_storage(bucket_name, source_blob_name):
    try:
        # Create credentials object from the dictionary
        credentials = Credentials.from_service_account_info(creds_dict)

        # Create a client to interact with the Google Cloud Storage API
        storage_client = storage.Client(credentials=credentials, project=creds_dict["project_id"])

        # Get the bucket where the file is stored
        bucket = storage_client.get_bucket(bucket_name)

        blobs = bucket.list_blobs(prefix=source_blob_name)

        csv_data = None
        blob_name = None

        # this way we are only keeping the first blob
        for blob in blobs:
            # Download the file content as a string
            csv_data = blob.download_as_text()
            blob_name = blob.name
            break
        
        if csv_data is not None:
            # Use pandas to read the CSV data
            df = pd.read_csv(StringIO(csv_data))
        else:
            df = pd.DataFrame()

        return df, blob_name

    except NotFound:
        print(f"The file '{source_blob_name}' does not exist in the bucket '{bucket_name}'.")
        return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def delete_file_from_cloud_storage(bucket_name, blob_name):
    try:
        # Create credentials object from the dictionary
        credentials = Credentials.from_service_account_info(creds_dict)

        # Create a client to interact with the Google Cloud Storage API
        storage_client = storage.Client(credentials=credentials, project=creds_dict["project_id"])

        # Get the bucket where the file is stored
        bucket = storage_client.get_bucket(bucket_name)

        blobs = bucket.list_blobs(prefix=blob_name)

         # this way we are only keeping the first blob
        for blob in blobs:
            # Delete the blob
            blob.delete()
            break

        print(f"File '{blob_name}' successfully deleted from bucket '{bucket_name}'.")
        return True

    except NotFound:
        print(f"The file '{blob_name}' does not exist in the bucket '{bucket_name}'.")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def upload_dataframe_to_cloud_storage(bucket_name, destination_blob_name, df):
    try:
        # Create credentials object from the dictionary
        credentials = Credentials.from_service_account_info(creds_dict)

        # Create a client to interact with the Google Cloud Storage API
        storage_client = storage.Client(credentials=credentials, project=creds_dict["project_id"])

        # Get the bucket where the file will be stored
        bucket = storage_client.get_bucket(bucket_name)

        # Convert DataFrame to CSV
        csv_data = df.to_csv(index=False)

        # Create a blob (file) in the bucket
        blob = bucket.blob(destination_blob_name)

        # Upload the CSV data to the blob
        blob.upload_from_string(csv_data, content_type='text/csv')

        print(f"DataFrame successfully uploaded to '{destination_blob_name}' in bucket '{bucket_name}'.")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def upload_text_file_to_cloud_storage(bucket_name, destination_blob_name, text):
    try:
        # Create credentials object from the dictionary
        credentials = Credentials.from_service_account_info(creds_dict)

        # Create a client to interact with the Google Cloud Storage API
        storage_client = storage.Client(credentials=credentials, project=creds_dict["project_id"])

        # Get the bucket where the file will be stored
        bucket = storage_client.get_bucket(bucket_name)

        # Create a blob (file) in the bucket
        blob = bucket.blob(destination_blob_name)

        # Upload the text to the blob
        blob.upload_from_string(text, content_type='text/plain')

        print(f"Text successfully uploaded to '{destination_blob_name}' in bucket '{bucket_name}'.")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def download_text_file_from_cloud_storage(bucket_name, source_blob_name):
    try:
        # Create credentials object from the dictionary
        credentials = Credentials.from_service_account_info(creds_dict)

        # Create a client to interact with the Google Cloud Storage API
        storage_client = storage.Client(credentials=credentials, project=creds_dict["project_id"])

        # Get the bucket where the file is stored
        bucket = storage_client.get_bucket(bucket_name)

        blobs = bucket.list_blobs(prefix=source_blob_name)

        text_data = None

        # this way we are only keeping the first blob
        for blob in blobs:
            # Download the file content as a string
            text_data = blob.download_as_text()
            break
        
        return text_data

    except NotFound:
        print(f"The file '{source_blob_name}' does not exist in the bucket '{bucket_name}'.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_date_from_blob_name(blob_name):
    # Regular expression to find the date in the blob name
    match = re.search(r'\d{4}-\d{2}-\d{2}', blob_name)

    if match:
        return match.group(0)
    else:
        return None
    
def get_text_between_comments(text, start_comment, end_comment):
    start_index = text.find(start_comment)
    if start_index == -1:
        return None  # Start comment not found
    end_index = text.find(end_comment, start_index + len(start_comment))
    if end_index == -1:
        return None  # End comment not found
    return text[start_index + len(start_comment):end_index].strip()

def read_md_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()