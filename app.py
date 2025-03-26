import streamlit as st
from functions import check_credentials, register_user, switch_page, login

st.set_page_config(page_title="TRIVIA", page_icon="🔑")

if "page" not in st.session_state:
    st.session_state["page"] = "login"  # Default to login page

# --------- LOGIN PAGE ---------

if st.session_state["page"] == "login":
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if username and password:

            user = check_credentials(username, password)
            
            if user:
                login('home', username)

            else:
                st.error("Invalid username or password!")
        else:
            st.error("Please enter both username and password.")

    st.markdown("---")
    if st.button("New User? Register Here"):
        switch_page("register")  # Switch to register page


# --------- REGISTRATION PAGE ---------

elif st.session_state["page"] == "register":
    st.title("Register")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type='password')

    # Button to submit registration
    if st.button("Register"):
        if new_username and new_password:
            # Register the new user
            registration_successful = register_user(new_username, new_password)
            
            if registration_successful:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists. Please choose a different one.")
        else:
            st.error("Please enter both username and password.")

    st.markdown("---")
    if st.button("Already have an account? Login Here"):
        switch_page("login")

# --------- HOME GAME ---------

if st.session_state["page"] == "home":
    st.write(f'hello, {st.session_state["username"]}')