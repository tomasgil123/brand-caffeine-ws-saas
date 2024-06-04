import streamlit as st

from dashboard.data_scripts.get_product_views import (upload_product_views, get_product_views)

from dashboard.charts.page_views_charts import (generate_page_views_chart_by_category_last_12_months,
                                                generate_pageviews_orders_ratio_chart, 
                                                generate_page_views_evolution_last_12_months_by_category,
                                                generate_page_views_and_ratio_by_category_with_selector, 
                                                generate_conversion_rate_chart_by_category,
                                                generate_page_views_and_ratio_by_product_with_selector)

from dashboard.utils import (is_cookie_expired, get_date_from_blob_name)

def create_page_views_section(selected_client, type_plan):
    df_page_views, blob_name = get_product_views(client_name=selected_client)

    # id dataframe is empty tell user to click the update button
    if df_page_views is None or df_page_views.empty:
        st.write("No page views data available. Click the button below to update the data.")

    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")           
    
    if st.button("Update page views data"):
        # if st.session_state["user_cookie"] is empty display an error message
        if "user_cookie" not in st.session_state:
            st.error("Please, go to the 'Account' section and enter a cookie value.")
            return
        # we check if the cookie is expired
        is_expired = is_cookie_expired(st.session_state["user_cookie"])
        if is_expired:
            st.error("The cookie is expired. Please, go to the 'Account' section and enter a new cookie value.")
            return
        with st.spinner('Updating page views data...'):
            result = upload_product_views(client_name=selected_client, cookie=st.session_state["user_cookie"])
            if result:
                st.success('Page views updated!')
                st.experimental_rerun()
            else:
                st.error('An error occurred while updating the page views data.')
    
    
    if not df_page_views.empty:
        generate_page_views_chart_by_category_last_12_months(data=df_page_views, date_last_update=date_last_update)

        generate_page_views_evolution_last_12_months_by_category(data=df_page_views)

        generate_conversion_rate_chart_by_category(data_original=df_page_views, date_last_update=date_last_update)

        generate_pageviews_orders_ratio_chart(data_original=df_page_views, date_last_update=date_last_update)

        generate_page_views_and_ratio_by_category_with_selector(data_original=df_page_views)

        generate_page_views_and_ratio_by_product_with_selector(data_original=df_page_views)