import streamlit as st
from api import login
cols = st.columns([1,3,1])
with cols[1]:
    st.header("Login/Register")
    user_name=st.text_input("USER NAME ",placeholder="Enter user name")
    password = st.text_input("PASSWORD",placeholder="Enter your password",type='password')
    is_checked = st.checkbox("Accept Terms and Conditions")
    is_clicked=st.button("Login",type="primary",use_container_width=True)
    if is_clicked:
        if user_name and password and is_checked:
            data=login(user_name,password)
            if data:
                st.toast("login successful")
            else:
                st.toast("invalid login credentials")
        else:
            st.toast("Please fill the form")          



