import streamlit as st

from dashboard.account import build_account_dashboard
from dashboard.product_listings_section import create_product_listings_section
from dashboard.email_marketing_section import create_email_marketing_section
from dashboard.competitors_section import create_competitors_section
from dashboard.review_optimization_section import create_review_optimization_section

def create_dashboard(selected_client, selected_report, type_plan, brand_name_in_faire):
    if selected_report == "Account":
        st.markdown("""
                # Account
                """)
        build_account_dashboard(selected_client, brand_name_in_faire)
        
    if selected_report == "Recommendations for Review Optimization":
        
        st.markdown("""
                # Recommendations for Review Optimization
                """)
        create_review_optimization_section(selected_client)
    
    if selected_report == "Recommendations to Improve Email Marketing":

        st.markdown("""
                # Recommendations to Improve Email Marketing
                """)
        create_email_marketing_section(selected_client, type_plan, brand_name_in_faire)
    
    if selected_report == "Recommendations for Outranking Competitors":

        st.markdown("""
                # Recommendations for Outranking Competitors
                """)
        create_competitors_section(selected_client, brand_name_in_faire)

    if selected_report == "Recommendations for Product Listing Optimization":
        
        st.markdown("""
                # Recommendations for Product Listing Optimization
                """)
        create_product_listings_section(selected_client, type_plan)
        
        