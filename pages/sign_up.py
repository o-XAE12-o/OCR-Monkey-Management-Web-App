import streamlit as st
import functions_obs as fn
from time import sleep

st.image("logo.png")
st.title("Sign-up page")
if st.button("Back"):
    st.session_state.logged_in = False
    st.markdown("""
            <meta http-equiv="refresh" content="0; url='http://localhost:8501/login_page'" />
            """, unsafe_allow_html=True)
st.session_state.logged_in = False

with st.form("sign up"):
    first_name = st.text_input("Enter your first name")
    user_new = st.text_input("Enter Email")
    ver = fn.is_valid_email(user_new)
    exists = fn.user_exists(user_new)

    if ver:
        if user_new == "":
            pass
        else:
            if exists:
                st.warning("User exists already")
                return_login = st.page_link(label="Have account?", page="http://localhost:8501/login_page")
            else:
                pw_new = st.text_input("Enter Password", type='password')
                st.markdown(
                    """
                    Make sure the password consists of:
                    - At least 1 capital and lowercase character
                    - At least 1 special character
                    - At least 1 number
                    """
                )
                if not fn.is_valid_pw(pw_new):
                    st.warning("Password criteria not met")
                else:
                    if pw_new == "":
                        pass
                    else:
                        pw_confirm = st.text_input("Enter Password again", type='password')
                        if pw_confirm == "":
                            pass
                        else:
                            if pw_confirm == pw_new:
                                if fn.sign(True):
                                    username = fn.store_user_with_generated_username(first_name, user_new, pw_new)
                                    st.info(f"Account Created! Your username is {username}")
                                    st.session_state.username = username  # Store username in session state
                                    submit = st.form_submit_button()
                                    if submit:
                                        st.session_state.logged_in = True
                                        st.success("Logged in successfully!")
                                        sleep(1)
                                        st.switch_page("homepage.py")
                            else:
                                st.warning("Passwords do not match")
    else:
        st.warning("Invalid Email format")
    submit = st.form_submit_button()