import streamlit as st

from dashboard.account import build_account_dashboard
from dashboard.page_views_section import create_page_views_section
from dashboard.email_marketing_section import create_email_marketing_section

def create_dashboard(selected_client, selected_report, type_plan, brand_name_in_faire):
    if selected_report == "Account":
        st.markdown("""
                # Account
                """)
        build_account_dashboard()
        
    if selected_report == "Page views":

        st.markdown("""
                # Page Views
                """)
        create_page_views_section(selected_client, type_plan)
    
    if selected_report == "Email marketing analytics":
        st.markdown("""
                # Email Marketing Analytics
                """)
        create_email_marketing_section(selected_client, type_plan, brand_name_in_faire)
        
        