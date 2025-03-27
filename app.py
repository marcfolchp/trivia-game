import streamlit as st
from functions import check_credentials, register_user, switch_page, login, create_question, add_one
import time

st.set_page_config(page_title="TRIVIA", page_icon="🔑")

if "page" not in st.session_state:
    #st.session_state["page"] = "login"  # Default to login page
    st.session_state["page"] = "home"
    st.session_state["username"] = "admin"

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

    time.sleep(5)

    question = create_question()

    st.markdown(f"<h1 style='text-align: center;'>{question['question']} --- {question['category']}</h1>", unsafe_allow_html=True)

    a, b, c, d = st.columns([10, 3, 3, 10])

    # Place the True button in the first column
    with b:
        if st.button("True"):
            if question['answer'] == True:
                add_one(st.session_state["username"], question['category'])
                add_one(st.session_state["username"], f"total")
            else:
                add_one(st.session_state["username"], f"total")

    # Place the False button in the right column, centered
    with c:
        if st.button("False"):
            if question['answer'] == False:
                add_one(st.session_state["username"], question['category'])
                add_one(st.session_state["username"], f"total")
            else:
                add_one(st.session_state["username"], f"total")
