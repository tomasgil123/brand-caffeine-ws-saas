import streamlit as st

def build_account_dashboard():
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


