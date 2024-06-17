import streamlit as st

from dashboard.global_utils import (is_cookie_expired, get_brand_token)
from dashboard.data_scripts.get_marketing_campaign_info import (upload_marketing_info)
from dashboard.data_scripts.get_product_views import (upload_product_views)
from dashboard.data_scripts.get_competitors_data import (upload_competitors_info, get_competitors_data, 
                                                         upload_competitors_recommendations_main_attributes,
                                                         upload_competitors_summary_main_attributes)
from dashboard.data_scripts.get_reviews import (upload_reviews_data)
from dashboard.data_scripts.get_orders import (upload_orders_info)

from dashboard.charts.competitors_charts_utils import (get_main_attributes)
from dashboard.utils_chatgpt import OpenaiInsights

from dashboard.recommendations.email_marketing import upload_marketing_recommendations
from dashboard.recommendations.reviews import upload_reviews_recommendations

def build_account_dashboard(selected_client, brand_name_in_faire):
    st.markdown("""
                ### Enter your Faire cookie
                """)
    # Input field for the user to enter a cookie
    user_cookie = st.text_input("Enter a cookie value:", key="user_cookie_input")

    # Button to save the cookie
    if st.button("Save", key="user_cookie_btn"):
        if user_cookie:
            # Save the cookie in session state
            st.session_state["user_cookie"] = user_cookie
            st.success("Cookie saved successfully!")
        else:
            st.error("Please enter a cookie value.")
    
    # we add some empty space
    st.write("")
    st.write("")

    st.markdown("""
                ### Data
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

    if st.button("Update Faire orders data"):
        # if st.session_state["user_cookie"] is empty display an error message
        if "user_cookie" not in st.session_state:
            st.error("Please, go to the 'Account' section and enter a cookie value.")
            return
        # we check if the cookie is expired
        is_expired = is_cookie_expired(st.session_state["user_cookie"])
        if is_expired:
            st.error("The cookie is expired. Please, go to the 'Account' section and enter a new cookie value.")
            return
        with st.spinner('Updating orders data...'):
            brand_token = get_brand_token(brand_name=brand_name_in_faire, cookie=st.session_state["user_cookie"])
            if brand_token is None:
                st.error("Brand name doesn't seem to belong a a brand currently in Faire.")
                return
            else:
                result = upload_orders_info(brand_token=brand_token, client_name=selected_client, cookie=st.session_state["user_cookie"])
                if result:
                    st.success('Orders info updated!')
                    st.experimental_rerun()
                else:
                    st.error('An error occurred while updating the orders data.')

    if st.button("Update Faire reviews data"):
        if "user_cookie" not in st.session_state:
            st.error("Please, go to the 'Account' section and enter a cookie value.")
            return
        # we check if the cookie is expired
        is_expired = is_cookie_expired(st.session_state["user_cookie"])
        if is_expired:
            st.error("The cookie is expired. Please, go to the 'Account' section and enter a new cookie value.")
            return
        with st.spinner('Updating reviews data...'):
            brand_token = get_brand_token(brand_name=brand_name_in_faire, cookie=st.session_state["user_cookie"])
            if brand_token is None:
                st.error("Brand name doesn't seem to belong a a brand currently in Faire.")
                return
            else:
                result = upload_reviews_data(brand_token=brand_token, client_name=selected_client, cookie=st.session_state["user_cookie"])
                if result:
                    st.success('Reviews info updated!')
                    st.experimental_rerun()
                else:
                    st.error('An error occurred while updating the reviews data.')
    
    # we add some empty space
    st.write("")
    st.write("")

    # Roma Leathers, Sarta, Sixtease Bags USA, Threaded Pear
    competitors = st.text_input("Enter a competitor names: (split with , )", key="competitor_names")

    if st.button("Update Faire competitors data"):
        if "user_cookie" not in st.session_state:
            st.error("Please, go to the 'Account' section and enter a cookie value.")
            return
        # if there are no competitors display an error message
        if not competitors:
            st.error("Please enter at least one competitor name.")
            return
        # we add to competitors the name of the client
        competitors = competitors.split(",")
        competitors.append(brand_name_in_faire)
        # we get for each brand its brand token
        brands_tokens = []
        with st.spinner('Checking brands are in Faire...'):
            for brand_name in competitors:
                brand_token = get_brand_token(brand_name=brand_name, cookie=st.session_state["user_cookie"])
                if brand_token is not None:
                    brands_tokens.append(brand_token)
        
        if len(brands_tokens) > 1:
            with st.spinner('Updating competitors data...'):
                result = upload_competitors_info(client_name=selected_client,brand_ids=brands_tokens)
                if result:
                    st.success('Competitors data updated!')
                    st.experimental_rerun()
                else:
                    st.error('An error occurred while updating the competitors data.')
        else:
            st.error("None of the brands entered seem to be currently present in Faire.")
            return
    st.markdown("""
                ### Recommendations
                """)
    if st.button("Create competitors recommendations"):
        df_competitors, _ = get_competitors_data(selected_client)

        df_main_attributes = get_main_attributes(df_competitors)

        insights = OpenaiInsights()
        string_dataframe = df_main_attributes.to_string(index=False)

        chatgpt_insights_summary_main_attributes = insights.generate_insights({"prompt_name": "Competitors - main attributes - summary", "brand_name": brand_name_in_faire, "string_data": string_dataframe})
        chatgpt_insights_recommendations_main_attributes = insights.generate_insights({"prompt_name": "Competitors - main attributes - recommendations", "brand_name": brand_name_in_faire, "string_data": string_dataframe})

        upload_competitors_summary_main_attributes(client_name=selected_client, text=chatgpt_insights_summary_main_attributes)
        upload_competitors_recommendations_main_attributes(client_name=selected_client, text=chatgpt_insights_recommendations_main_attributes)

    if st.button("Create email marketing recommendations"):
        if "user_cookie" not in st.session_state:
            st.error("Please, go to the 'Account' section and enter a cookie value.")
            return
        upload_marketing_recommendations(client_name=selected_client, cookie=st.session_state["user_cookie"])

    if st.button("Create reviews recommendations"):
        if "user_cookie" not in st.session_state:
            st.error("Please, go to the 'Account' section and enter a cookie value.")
            return
        
        upload_reviews_recommendations(client_name=selected_client, cookie=st.session_state["user_cookie"])