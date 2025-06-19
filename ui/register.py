import streamlit as st
from ui.check_and_add import AddUser

def rigister() -> bool:
    fristName : str = st.text_input("Enter Your Frist Name")
    lastName: str = st.text_input("Enter Your Last Name")
    email : str = st.text_input("Enter Your Email")
    password : str = st.text_input("Enter Your Password")

    if st.button("Register") :
        if fristName and lastName and email and password:
            user : AddUser = AddUser(fristName=fristName, lastName=lastName, email=email, password=password)
            check = user.check_user()
            user.after_addcheck()

            if check:
                st.warning("Please Change Your Email And Password")
            else:
                push_user_data = user.add_user()
                if push_user_data:
                    st.success("Registered Successfully")
                    return True
                else:
                    st.warning("Somethink Was Wrong Please Check Your Information")
                    
                    
 

       