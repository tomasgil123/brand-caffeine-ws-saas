import pandas as pd
from datetime import datetime

from dashboard.data_scripts.get_competitors_data_utils import get_brands_data
from dashboard.utils import (upload_dataframe_to_cloud_storage, delete_file_from_cloud_storage, 
                             download_csv_from_cloud_storage, upload_text_file_to_cloud_storage, download_text_file_from_cloud_storage)

# vamos a tener dos recommendations:
# - en base a los main attributes
# - en base a los brand values

# vamos a tener dos summaries: => cada summary va a estar acompanado por un chart
# - en base a los main attributes
# - en base a los brand values

def get_competitors_data(client_name):

    # Get the data from the Google Cloud Storage bucket
    bucket_name = "faire_competitors"
    source_blob_name = f"{client_name}"

    df_competitors, blob_name = download_csv_from_cloud_storage(bucket_name, source_blob_name)

    # df_competitors is None we return an empty dataframe
    if df_competitors is None:
        return pd.DataFrame(), None
    else:
        return df_competitors, blob_name

def upload_competitors_info(client_name, brand_ids):
    bucket_name = "faire_competitors"

    current_date = datetime.now().strftime("%Y-%m-%d")
    source_blob_name_orders = f"{client_name}_{current_date}.csv"

    brands_data = get_brands_data(brand_ids)
    df_competitors = pd.DataFrame(brands_data)

    # we delete previous file
    delete_file_from_cloud_storage(bucket_name, f"{client_name}")

    return upload_dataframe_to_cloud_storage(bucket_name, source_blob_name_orders, df_competitors)


# main attributes

def upload_competitors_recommendations_main_attributes(client_name, text):
    bucket_name = "faire_competitors"
    source_blob_name = f"{client_name}_recommendations_main_attributes.txt"

    return upload_text_file_to_cloud_storage(bucket_name, source_blob_name, text)

def get_competitors_recommendations_main_attributes(client_name):
    bucket_name = "faire_competitors"

    source_blob_name = f"{client_name}_recommendations_main_attributes"

    return download_text_file_from_cloud_storage(bucket_name, source_blob_name)


def upload_competitors_summary_main_attributes(client_name, text):
    bucket_name = "faire_competitors"
    source_blob_name = f"{client_name}_summary_main_attributes.txt"

    return upload_text_file_to_cloud_storage(bucket_name, source_blob_name, text)

def get_competitors_summary_main_attributes(client_name):
    bucket_name = "faire_competitors"

    source_blob_name = f"{client_name}_summary_main_attributes"

    return download_text_file_from_cloud_storage(bucket_name, source_blob_name)

# brand values

def upload_competitors_recommendations_brand_values(client_name, text):
    bucket_name = "faire_competitors"
    source_blob_name = f"{client_name}_recommendations_brand_values.txt"

    return upload_text_file_to_cloud_storage(bucket_name, source_blob_name, text)

def get_competitors_recommendations_brand_values(client_name):
    bucket_name = "faire_competitors"

    source_blob_name = f"{client_name}_recommendations_brand_values"

    return download_text_file_from_cloud_storage(bucket_name, source_blob_name)

def upload_competitors_summary_brand_values(client_name, text):
    bucket_name = "faire_competitors"
    source_blob_name = f"{client_name}_summary_brand_values.txt"

    return upload_text_file_to_cloud_storage(bucket_name, source_blob_name, text)

def get_competitors_summary_brand_values(client_name):
    bucket_name = "faire_competitors"

    source_blob_name = f"{client_name}_summary_brand_values"

    return download_text_file_from_cloud_storage(bucket_name, source_blob_name)