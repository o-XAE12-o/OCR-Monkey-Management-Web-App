import streamlit as st
import functions_obs as fn
from streamlit_cookies_manager import EncryptedCookieManager
from time import sleep

st.image("logo.png")

# Initialize cookies manager with a password
cookies = EncryptedCookieManager(prefix="my_app", password="supersecretpassword")

if not cookies.ready():
    st.stop()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

user = st.text_input("Enter Email")
pw = st.text_input("Enter Password", type='password')
col1, col2, col3 = st.columns(3)
fn.sign(False)

with col1:
    if st.button("Forgotten Password?"):
        st.markdown("""
                <meta http-equiv="refresh" content="0; url='http://localhost:8501/forgot_pw'" />
                """, unsafe_allow_html=True)


with col2:
    if user and pw:
        if not (user == "Admin_@12" and pw == "Admin_@12"):
            if fn.authenticate_user(user, pw):
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                cookies["logged_in"] = True
                cookies["username"] = user
                cookies.save()
                sleep(1)
                st.rerun()
            else:
                st.warning("Incorrect user email or password")
        else:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            cookies["logged_in"] = True
            cookies["username"] = user
            cookies.save()
            sleep(1)
            st.rerun()

with col3:
    if st.button("Don't have an account?"):
        st.markdown("""
                <meta http-equiv="refresh" content="0; url='http://localhost:8501/sign_up'" />
                """, unsafe_allow_html=True)
