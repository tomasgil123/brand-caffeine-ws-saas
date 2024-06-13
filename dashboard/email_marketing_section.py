import streamlit as st
import pandas as pd

from dashboard.data_scripts.get_marketing_campaign_info import (get_marketing_info)

from dashboard.charts.email_marketing_charts import (get_email_marketing_kpis_last_30_days, 
                                              get_email_marketing_kpis_by_month, sales_by_month)

from dashboard.utils import ( get_date_from_blob_name)

def create_email_marketing_section(selected_client, type_plan, brand_name_in_faire):

    df_email_marketing, blob_name = get_marketing_info(client_name=selected_client)

    # id dataframe is empty tell user to click the update button
    if df_email_marketing is None or df_email_marketing.empty:
        st.write("No email marketing data available. Go to the 'Account' section to update it.")
    
    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    if not df_email_marketing.empty:

        date_last_update = pd.to_datetime(date_last_update)
        st.markdown("""
                ### Email performance review
                Last 30 days:
                """)
        get_email_marketing_kpis_last_30_days(df_email_marketing, date_last_update)

        get_email_marketing_kpis_by_month(df_email_marketing)

        sales_by_month(df_email_marketing, 'open_based_total_order_value', 'Total Sales Open emails (12 months)', date_last_update)
        sales_by_month(df_email_marketing, 'click_based_total_order_value', 'Total Sales Click emails (12 months)', date_last_update)