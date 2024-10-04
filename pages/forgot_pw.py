import streamlit as st
import functions_obs as fn
import courier
from time import sleep, time
from courier.client import Courier

st.image("logo.png")
st.title("Password Reset")

# Add Back Button
if st.button("Back"):
    st.session_state.logged_in = False
    st.markdown("""
                <meta http-equiv="refresh" content="0; url='http://localhost:8501/login_page'" />
                """, unsafe_allow_html=True)

st.session_state.logged_in = False

if 'ver_code' not in st.session_state:
    st.session_state['ver_code'] = fn.ver_code()
    st.session_state['ver_code_time'] = time()

expiry_time = 300  # 5 minutes in seconds
COURIER_API_KEY = "pk_prod_6DRTMXQ27JMRS4HGHHCCZ8C3MJJK"

with st.form("password_reset"):
    email = st.text_input("Enter email of account")
    if st.form_submit_button("Click to send verification code"):
        if email:  # Check if email is not empty
            username = fn.find_username_by_email(email)
            if username:
                st.session_state['ver_code'] = fn.ver_code()  # Update the verification code
                st.session_state['ver_code_time'] = time()  # Update the timestamp
                code = st.session_state['ver_code']
                client = Courier(authorization_token=COURIER_API_KEY)
                response = client.send(
                    message=courier.TemplateMessage(
                        template="FFM4ESSW9E49B5H73MXVG0HKQ5WA",
                        to=courier.UserRecipient(
                            email=email,
                            data={
                                "code": code,
                                "user": username,
                                "verification_code": code,
                                "expiry_time": "5 minutes",
                            }
                        ),
                    )
                )
                st.text("Verification code sent")
            else:
                st.warning("Email not found")
        else:
            st.warning("Please enter an email address")

with st.form("Enter verification code"):
    ver_code = st.text_input("Enter verification code")
    if st.form_submit_button("Submit"):
        current_time = time()
        if current_time - st.session_state['ver_code_time'] <= expiry_time:
            if ver_code == st.session_state['ver_code']:
                st.text("Valid!")
                st.session_state['verified'] = True
            else:
                st.title("Invalid")
        else:
            st.title("Verification code expired")

if st.session_state.get('verified', False):
    with st.form("new_password_form"):
        new_password = st.text_input("Enter new password", type='password')
        confirm_password = st.text_input("Confirm new password", type='password')
        st.markdown(
            """
            Make sure the password consists of:
            - At least 1 capital and lowercase character
            - At least 1 special character
            - At least 1 number
            """
        )
        if st.form_submit_button("Submit"):
            if new_password == confirm_password:
                if fn.is_valid_pw(new_password):
                    hashed_pwd = fn.hash_pw(new_password)
                    fn.save_user(username, hashed_pwd)
                    st.text("Password has been reset successfully!")
                    st.session_state.logged_in = True
                    st.success("Logged in successfully!")
                    sleep(1)
                    fn.switch_page("homepage")
                else:
                    st.text("Password criteria not met")
            else:
                st.text("Passwords do not match!")