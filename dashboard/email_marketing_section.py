import streamlit as st
import pandas as pd

from dashboard.data_scripts.get_marketing_campaign_info import (get_marketing_info, upload_marketing_info)

from dashboard.charts.email_marketing_charts import (get_email_marketing_kpis_last_30_days, 
                                              get_email_marketing_kpis_by_month, sales_by_month)

from dashboard.utils import (is_cookie_expired, get_date_from_blob_name, get_brand_token)

def create_email_marketing_section(selected_client, type_plan, brand_name_in_faire):

    df_email_marketing, blob_name = get_marketing_info(client_name=selected_client)

    # id dataframe is empty tell user to click the update button
    if df_email_marketing is None or df_email_marketing.empty:
        st.write("No email marketing data available. Click the button below to update the data.")
    
    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    if st.button("Update email marketing data"):
        # if st.session_state["user_cookie"] is empty display an error message
        if "user_cookie" not in st.session_state:
            st.error("Please, go to the 'Account' section and enter a cookie value.")
            return
        # we check if the cookie is expired
        is_expired = is_cookie_expired(st.session_state["user_cookie"])
        if is_expired:
            st.error("The cookie is expired. Please, go to the 'Account' section and enter a new cookie value.")
            return
        with st.spinner('Updating email marketing data...'):
            brand_token = get_brand_token(brand_name=brand_name_in_faire, cookie=st.session_state["user_cookie"])
            if brand_token is None:
                st.error("Brand name doesn't seem to belong a a brand currently in Faire.")
                return
            else:
                result = upload_marketing_info(brand_token=brand_token, client_name=selected_client, cookie=st.session_state["user_cookie"])
                if result:
                    st.success('Email marketing info updated!')
                    st.experimental_rerun()
                else:
                    st.error('An error occurred while updating the email marketing data.')

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