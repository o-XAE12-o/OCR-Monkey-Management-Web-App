import functions_obs as fn
import streamlit as st

from time import sleep

# Check if the user is logged in
if not st.session_state.get('logged_in', False):
    st.warning("You are not logged in. Redirecting to login page in 5 seconds...")
    sleep(2)
    st.markdown("""
                    <meta http-equiv="refresh" content="0; url='http://localhost:8501/login_page'" />
                    """, unsafe_allow_html=True)
else:
    st.title("Welcome to the Homepage")
    st.write(f"You are logged in as {st.session_state.username}!")

    st.markdown(
        """
        <style>
        .logout-button {
            position: fixed;
            bottom: 10px;
            right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("Logout", key="logout", help="Click to logout",
                 on_click=lambda: st.session_state.update(logged_in=False)):
        st.success("Logged out successfully!")
        sleep(1)
        st.rerun()