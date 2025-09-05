from streamlit_supabase_auth import login_form
import streamlit as st

def sign_in():
    session = login_form()
    if not session:
        return None
    st.query_params["page"] = ["success"]
    return session