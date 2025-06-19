import streamlit as st
import time
from assistant.agent import agent
import json

# ------------------ Streamlit Chainlit-Style UI ------------------

# Ye UI sirf frontend hai. Backend logic (agent/tool calls) aap khud integrate kar sakte hain.

# Page Config
def chatbot():

    # 🎨 Apply Custom CSS for Chat Styling
    st.markdown("""
        <style>
            /* Chat Container */
            .chat-container {
                max-width: 80%;
                margin: auto;
            }

            /* User Chat Bubble */
            .user-message {
                text-align: left;
                color: black;
                background: rgb(233, 230, 230);
                border-radius: 20px;
                padding: 10px;
                margin-bottom: 10px;
                width: 55%;
                margin-left: auto;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }

            /* AI Chat Bubble */
            .ai-message {
                text-align: left;
                color: white;
                background: #007bff;
                border-radius: 20px;
                padding: 10px;
                margin-bottom: 10px;
                width: 55%;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            
            /* Typing Animation */
            @keyframes typing {
                0% { opacity: 0.2; }
                50% { opacity: 1; }
                100% { opacity: 0.2; }
            }

            .typing-effect {
                display: inline-block;
                font-size: 16px;
                font-weight: bold;
                color: #007bff;
                animation: typing 1.5s infinite;
            }

            /* Clickable Links */
            .ai-message a {
                color: #ffffff;
                text-decoration: underline;
            }
            
            .ai-message a:hover {
                color: #ffeb3b;
            }
        </style>
    """, unsafe_allow_html=True)

#   is main current user ky name ko get kar raha ho
    with open("current_user_email_password.json", "r") as file:
        user_name = json.load(file)
        with open("personal_information.json", "r") as file:
            all_user_name = json.load(file)
            filter_user = list(filter(lambda x : x["email"] == user_name["email"] and x["password"] == user_name["password"], all_user_name ))
            filter_user_name = filter_user[0]["fristName"]

    st.markdown(f'<h1 style="text-align: center; color: white; background: linear-gradient(45deg, #007bff, #00c6ff); padding: 15px; border-radius: 8px;">🤖 AI Assistant for {filter_user_name}</h1>', unsafe_allow_html=True)

    
    # is ky andar user or AI ky chat save ho rahy hai
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    value = st.chat_input("💬 Ask something about...")  # user input

    if not st.session_state.chat_history:
        default_message = f"""
        👋 Hello {filter_user_name}!  
        I'm your personal assistant, here to help you manage your **To-Do List** and securely organize your **personal information** like preferences, details, and more.  
        Feel free to ask me anything — I'm ready when you are!
        """
        st.session_state.chat_history.append({"role": "AI", "message": default_message})


    if value:
        # chat_history ky andar user ka question jaraha hai
        st.session_state.chat_history.append({"role": "user", "message": value})

    if value:
        try:
            # is main jo chat history hai us ko format kar raha hai ho 
            converted_chat_history = [
                    {
                        "role": "assistant" if chat["role"].lower() == "ai" else chat["role"].lower(),
                        "content": chat["message"]
                    }
                    for chat in st.session_state.chat_history
                    if "I'm your personal assistant" not in chat["message"]  # filter out default greeting
                ]
            # converted_chat_history ko mein agent main send kar raha ho
            response = agent(prompt=converted_chat_history)
            ai_answer = response.final_output 
            print(converted_chat_history) 


            # ✅ Extracting AI Response Correctly
            if response:

                # Save AI Response in chat history
                st.session_state.chat_history.append({"role": "AI", "message": ai_answer})

            else:
                st.session_state.chat_history.append({"role": "AI", "message": "⚠️ AI did not return a valid response."})

        except Exception as e:
            st.session_state.chat_history.append({"role": "AI", "message": "⚠️ Please wait 5 minutes and try again."})


   
    # 🔹 **Display Chat History with Fix for Links or ye div nichy end ho raha hai**
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":  # is ky andar user ka question araha hai
            st.markdown(f'<div class="user-message">{chat["message"]}</div>', unsafe_allow_html=True)
        else:  # is ky andar AI ka response araha hai
            time.sleep(1)
            st.markdown(f'<div class="ai-message">{chat["message"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # end div

