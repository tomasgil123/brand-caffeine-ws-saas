import streamlit as st
import pandas as pd

from dashboard.data_scripts.get_competitors_data import (get_competitors_data, get_competitors_recommendations_main_attributes,
                                                         get_competitors_summary_main_attributes)
from dashboard.utils import get_date_from_blob_name
from dashboard.charts.competitors_charts import (number_reviews_per_brand, 
                                                 plot_radar_chart_competitors, 
                                                 get_competitors_minimum_order_data, 
                                                 get_competitors_fulfillment_data)

def create_competitors_section(selected_client, brand_name_in_faire):
    
    df_competitors, blob_name = get_competitors_data(selected_client)
    
    if df_competitors is None or df_competitors.empty:
        st.write("No competitors data available. Click the button below to update the data.")
    
    if blob_name is not None:
        date_last_update = get_date_from_blob_name(blob_name)
        if date_last_update is not None:
            st.write(f"Data last updated at: {date_last_update}")

    if not df_competitors.empty:

        st.markdown("""
                    #### Brands considered competitors:
                    """)
        filtered_brands = df_competitors[df_competitors['Brand Name'] != brand_name_in_faire]['Brand Name']
        brand_string = ', '.join(filtered_brands)
        st.write(brand_string)

        recommendations = get_competitors_recommendations_main_attributes(selected_client)

        if recommendations is not None:
            st.markdown("""
                    #### Recommendations:
                    """)
            st.write(recommendations)

        summary_main_attributes = get_competitors_summary_main_attributes(selected_client)
        if summary_main_attributes is not None:
            st.markdown("""
                    #### Main differences between your brand and competitors:
                    """)
            st.write(summary_main_attributes)

        
        plot_radar_chart_competitors(df_competitors)
        
        number_reviews_per_brand(df_competitors, brand_name_in_faire)

        get_competitors_minimum_order_data(df_competitors, brand_name_in_faire)

        get_competitors_fulfillment_data(df_competitors, brand_name_in_faire)

