import streamlit as st
from ui.register import rigister
from ui.login import login
from ui.chatbot import chatbot


## ye dashboard ko display hony ko manage kar raha hai
if "display" not in st.session_state:
    st.session_state.display = False # agar is ki value True hogi to login or register waly show hogy wana flase hogi to after_log_reg.py show hoga

# agar  st.session_state.display is value true hoye
if  st.session_state.display:

    tab1, tab2 = st.tabs(["Register", "Login"])


    with tab1:
        if rigister(): # agar user register ho gaya ho is rigister() main True aye ga 
                st.session_state.display = False
                st.rerun()  # ✅ Force rerun to go to after_log_reg
        else:
            pass

    with tab2:
        if login(): # agar user login ho gaya ho is login() main True aye ga 
                st.session_state.display = False
                st.rerun()  # ✅ Force rerun to go to after_log_reg
        else:
            pass

else:
    chatbot()




