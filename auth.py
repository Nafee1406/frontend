import Streamlit as st
from Supabase import create_client, client

supabase_url = "https://ctbpovmhgakrageabszx.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN0YnBvdm1oZ2FrcmFnZWFic3p4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExODM0OTksImV4cCI6MjA2Njc1OTQ5OX0.5m2mHTmV3rh8xPSPctGl20h1zSna8ZYd3wgplxMuMI0"
client = create_client(supabase_url, supabase_key)

st.set_page_config(page_title="Authentication", layout="centered")

auth_mode = st.radio("Choose Mode", ["Login", "Register"], horizontal=True)

if auth_mode == "Register":
    st.subheader("Register")

    fname = st.text_input("First Name", key="reg_fname")
    lname = st.text_input("Last Name", key="reg_lname")
    user_id = st.text_input("User ID (Email or Username)", key="reg_userid")
    password = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register", key="register_button"):
        if not fname or not lname or not user_id or not password:
            st.warning("All fields are required!")
        else:
            existing = client.table("users").select("*").eq("user_id", user_id).execute()
            if existing.data:
                st.warning("User already exists!")
            else:
                client.table("users").insert({
                    "user_id": user_id,
                    "first_name": fname,
                    "last_name": lname,
                    "password": password
                }).execute()
                st.success("Registered successfully! You can now login.")

# Login Mode
elif auth_mode == "Login":
    st.subheader("Login")

    login_id = st.text_input("User ID", key="login_userid")
    login_password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        login_data = client.table("users").select("*") \
            .eq("user_id", login_id).eq("password", login_password).execute()

        if login_data.data:
            st.success("Login successful!")
            st.session_state["user"] = login_data.data[0]
            st.session_state["page"] = "dashboard"
            st.rerun()
        else:
            st.error("Invalid login details. Please try again.")
