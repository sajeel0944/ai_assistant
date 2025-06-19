import streamlit as st
# from check_and_add import AddUser
from ui.check_and_add import AddUser

def login():
    email : str = st.text_input("Enter Your Email:")
    password : str = st.text_input("Enter Your Password:")

    if st.button("Login"):
        if email and password:
            user : AddUser = AddUser(email=email, password=password)
            check = user.check_user()
            user.after_addcheck()

            if check:
                st.success("Login Successfully")
                return True
            else:
                st.warning("Invaild Your email and password")
                return False
            
       