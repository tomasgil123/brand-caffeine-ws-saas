import streamlit as st

from dashboard.utils import (is_cookie_expired, get_brand_token)
from dashboard.data_scripts.get_marketing_campaign_info import (upload_marketing_info)
from dashboard.data_scripts.get_product_views import (upload_product_views)

def build_account_dashboard(selected_client, brand_name_in_faire):
    st.markdown("""
                ### Enter your Faire cookie
                """)
    # Input field for the user to enter a cookie
    user_cookie = st.text_input("Enter a cookie value:")

    # Button to save the cookie
    if st.button("Save"):
        if user_cookie:
            # Save the cookie in session state
            st.session_state["user_cookie"] = user_cookie
            st.success("Cookie saved successfully!")
        else:
            st.error("Please enter a cookie value.")
    
    st.markdown("""
                ##### Update your account data with the buttons below
                """)

    if st.button("Update Faire data"):
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
        with st.spinner('Updating page views data...'):
            result = upload_product_views(client_name=selected_client, cookie=st.session_state["user_cookie"])
            if result:
                st.success('Page views updated!')
                st.experimental_rerun()
            else:
                st.error('An error occurred while updating the page views data.')


