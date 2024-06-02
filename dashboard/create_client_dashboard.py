import streamlit as st

def create_dashboard(selected_client, selected_report):
    if selected_report == "Account":
        st.markdown("""
                # Account
                ### Enter your Faire cookie
                """)
        
    if selected_report == "Sales":
        st.markdown("""
                # Sales
                ### Data about sales
                """)
   