import streamlit as st

from dashboard.account import build_account_dashboard
from dashboard.page_views_section import create_page_views_section

def create_dashboard(selected_client, selected_report, type_plan):
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
        
        