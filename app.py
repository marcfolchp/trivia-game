import streamlit as st
from functions import check_credentials, register_user, switch_page, login, create_question, handle_answer, global_ranking, user_stats
import time
import pandas as pd

st.set_page_config(page_title="TRIVIA", page_icon="🔑")

if "page" not in st.session_state:
    st.session_state["page"] = "login"  # Default to login page
    # st.session_state["page"] = "home"
    # st.session_state["username"] = "admin"

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

pastel_colors = [
    "#FFDDC1",  # Soft Peach
    "#FFABAB",  # Light Pink
    "#FFC3A0",  # Warm Apricot
    "#D5AAFF",  # Soft Lavender
    "#85E3FF",  # Light Blue
    "#B9FBC0",  # Pastel Green
    "#FF9CEE",  # Light Magenta
    "#FCE38A",  # Pale Yellow
]

if st.session_state["page"] == "home":
    
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = create_question()

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    selected_tab = st.sidebar.radio("Go to:", ["Home", "My Stats", "Global Ranking"])

    if selected_tab == "Home":
        # Home Page: Question Answering
        question = st.session_state["current_question"]  # Use the stored question

        st.markdown(f"<h1 style='text-align: center;'>{question['question']}</h1>", unsafe_allow_html=True)

        a, b, c, d = st.columns([10, 4, 4, 10])

        with b:
            if st.button("True"):
                handle_answer(True, question)

        with c:
            if st.button("False"):
                handle_answer(False, question)

    elif selected_tab == "My Stats":
        # Display user stats (Replace with your actual function)
        st.header("My Stats")
        user_stats = user_stats(st.session_state["username"])

        cols_per_row = 2  # Adjust this to fit more or fewer tabs in a row
        categories = list(user_stats.keys())

        for i in range(0, len(categories), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(categories):
                    category = categories[i + j]
                    accuracy, total = user_stats[category]
                    bg_color = pastel_colors[i + j % len(pastel_colors)]  # Assign a pastel color

                    with cols[j]:
                        # Add space above each container
                        st.write("")  

                        with st.container():
                            # Display category name inside a colored container
                            st.markdown(
                                f"""
                                <div style="background-color: {bg_color}; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px;">
                                    <h3 style="margin-bottom: 5px;">{category}</h3>
                                    <p style="font-size: 20px; font-weight: bold; color: darkgreen;">{accuracy * 100:.1f}% Correct</p>
                                    <p style="font-size: 14px; color: gray;">Total Answered: {total}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        # Add space below each container
                        st.write("")

        # user_stats = get_user_stats(st.session_state["username"])  # Fetch stats from your database
        # st.write(user_stats)

    elif selected_tab == "Global Ranking":
        # Display leaderboard (Replace with your actual function)
        st.header("Global Ranking")
        # leaderboard = get_global_ranking()  # Fetch ranking from your database

        current_user = st.session_state["username"]

        # Start HTML table
        styled_table = "<table style='width:100%; border-collapse: collapse;'>"
        styled_table += "<tr><th>Username</th><th>Questions Taken</th><th>Percentage Correct</th></tr>"

        # Generate table rows with styling for the current user
        for _, row in global_ranking().iterrows():
            if row["Username"] == current_user:
                styled_table += (
                    f"<tr style='font-weight: bold; background-color: lightyellow;'>"
                    f"<td>{row['Username']}</td>"
                    f"<td>{row['Questions Taken']}</td>"
                    f"<td>{row['Percentage Correct']}</td></tr>"
                )
            else:
                styled_table += (
                    f"<tr><td>{row['Username']}</td>"
                    f"<td>{row['Questions Taken']}</td>"
                    f"<td>{row['Percentage Correct']}</td></tr>"
                )

        # Close HTML table
        styled_table += "</table>"

        # Display table
        st.markdown(styled_table, unsafe_allow_html=True)