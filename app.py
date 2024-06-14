import os
import hmac
import streamlit as st
import pandas as pd

from dashboard.create_client_dashboard import create_dashboard
# from utils import save_user_log
from dashboard.utils import get_data_from_google_spreadsheet

openai_api_key = st.secrets["openai_api_key"]

if openai_api_key != "":
    os.environ['OPENAI_API_KEY'] = openai_api_key

with open("custom.css") as f:
    custom_css = f.read()

# Use st.markdown to inject the CSS
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

def get_all_files_in_directory(directory):
    files = []
    # os.walk returns a generator, that creates a tuple of values
    # (current_path, directories in current_path, files in current_path).
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            files.append(os.path.join(dirpath, file))
    return files

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""

        spreadsheet_id = "18J3yz4i1TNLUH3KQ-gOyjZipnwZhp1lHvLNX58Y7vlk"
        worksheet_name = "Sheet1"

        # df_credentials has two columns "user" and "password"
        df_credentials = get_data_from_google_spreadsheet(spreadsheet_id, worksheet_name)

        df_credentials = df_credentials[df_credentials['user'] == st.session_state["username"]]
        # if dataframe is empty it means user doesn't exist
        if df_credentials.empty:
            st.session_state["user_exists"] = False
            return
        else:
            st.session_state["user_name"] = st.session_state["username"]
            st.session_state["plan"] = df_credentials['plan'].values[0]
            st.session_state["brand_name_in_faire"] = df_credentials['brand_name_in_faire'].values[0]
            st.session_state["user_exists"] = True

        # if password is correct
        if hmac.compare_digest(df_credentials['password'].values[0], st.session_state["password"]):
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    st.title("Login to Brand Caffeine analytics dashboard")
    login_form()
    if "user_exists" in st.session_state and not st.session_state["user_exists"]:
        st.error("😕 User doesn't seem to exist")
    elif "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password doesn't seem to be correct")
    return False


if not check_password():
    st.stop()

# Main Streamlit app starts here
    
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
            margin-top: -75px;
        }
    </style>
    """, unsafe_allow_html=True
)
st.sidebar.image('brand_caffeine_logo.png', caption='', width=150)

# save_user_log(st.session_state["user_name"])

report_options = ['Account','Recommendations for Outranking Competitors', 'Recommendations to Improve Email Marketing', 'Recommendations for Review Optimization']

default_report_option = report_options[0]

st.sidebar.title(st.session_state['user_name'])

report_option_selected = st.sidebar.radio("Select an app section", options=report_options, index=report_options.index(default_report_option), key = 2)

create_dashboard(selected_client=st.session_state["user_name"], selected_report=report_option_selected, type_plan=st.session_state["plan"], brand_name_in_faire=st.session_state["brand_name_in_faire"])