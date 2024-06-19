import streamlit as st
import pandas as pd

from dashboard.data_scripts.get_competitors_data import (get_competitors_data, get_competitors_recommendations_main_attributes,
                                                         get_competitors_summary_main_attributes)
from dashboard.global_utils import get_date_from_blob_name
from dashboard.charts.competitors_charts import (number_reviews_per_brand, 
                                                 plot_radar_chart_competitors, 
                                                 get_competitors_minimum_order_data, 
                                                 get_competitors_fulfillment_data)

def create_competitors_section(selected_client, brand_name_in_faire):
    
    df_competitors, blob_name = get_competitors_data(selected_client)
    
    if df_competitors is None or df_competitors.empty:
        st.write("No competitors data available. Go to the 'Account' section to update it.")
    
    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    if not df_competitors.empty:
        st.write("")
        st.write("")
        st.write("This page is dedicated to helping you understand how your business compares to your competitors on Faire. We’ve included your customized, analytics-based optimization recommendations, as well as general, but strongly advised, changes you can make to be as successful as possible on Faire.")

        recommendations = get_competitors_recommendations_main_attributes(selected_client)

        if recommendations is not None:
            st.markdown("""
                    #### Customized Recommendations:
                    """)
            st.write(recommendations)

        st.markdown("""
            #### Brands considered competitors:
        """)
        # we filter brand_name_in_faire from the list of competitors
        df_competitors_list = df_competitors[df_competitors['Brand Name'] != brand_name_in_faire]
        for index, row in df_competitors_list.iterrows():
            st.markdown(f"- [{row['Brand Name']}](https://www.faire.com/brand/{row['Brand Token']}) - {row['Description']}")

        summary_main_attributes = get_competitors_summary_main_attributes(selected_client)
        if summary_main_attributes is not None:
            st.markdown("""
                    #### Recommendation Details:
                    """)
            st.write(summary_main_attributes)


        

        
        # plot_radar_chart_competitors(df_competitors)
        
        number_reviews_per_brand(df_competitors, brand_name_in_faire)

        get_competitors_minimum_order_data(df_competitors, brand_name_in_faire)

        get_competitors_fulfillment_data(df_competitors, brand_name_in_faire)

