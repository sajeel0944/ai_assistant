from agents import function_tool
import json
from datetime import datetime


#---------------------------------function_tool------------------------------------------------


@function_tool
def AddTask(task : str, priority: str) -> bool: # task user dyga or priority llm select karky dy ga
    """
    # Add a new task to the todo list.

    ## Parameters:
    - ***task (str)*** : User ka diya gaya task.
    - ***priority (str)*** : ye LLm select karry ga ky is ki priority kia hai LLM user sy nhi pouch ga or 
    Tum AI ke taur par estimate karo ke task ki importance kya hai.
    
    ### Instructions:
    1. Pehle user ka task text parho.
    2. Samjho uska urgency aur importance.
    3. Phir in 5 options me se best priority select karo:

        - "low"
        - "medium"
        - "high"
        - "urgent"
        - "none"

    Sirf AI hi decide karega ke kaunsi priority assign karni chahiye.

    """
        
    # is ky andar current_user_email_password.json sy current user ka email or password get kar raha ho
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai

        after_add : list[dict] = [] # is main current user ky new task add ho ky is mian aye ga

        with open("personal_information.json" , "r") as file:
            all_user = json.load(file)

            for user_data in all_user: # is main ek ek karky sary user is main aye gy
                if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho
                    current_user_todo = user_data["todoList"] # is main current user ka todo list aye ga

                    if current_user_todo: # agar current user ky todoList ky andar pahly sy todo list ho to ye chaly ga
                        get_last_todo : dict = current_user_todo[-1] # is ky andar current_user_todo ka last wala task aye ga 
                        get_last_tastNo : int = get_last_todo["taskNo"] # is main us last waly ky task number get kia 
                        task_no : int = get_last_tastNo + 1 # is main us last waly main 1 plus kia or is number ko new_todo ky taskNo main dia

                        new_todo : dict = {
                            "taskNo": task_no,
                            "text": task, # is main user ka task aye ga
                            "addDate" : f"{datetime.now().strftime("%Y-%m-%d")}", # jab user new task add kar ry ga us din ki date aye gi,
                            "priority": priority, # is main llm jo select kar lyga wo is main aye ga
                            "completed": False
                        }
                        user_data["todoList"].append(new_todo) # is main user_data ky todoList main new task add kia
                        after_add.append(user_data) # is main current user ka pora data after_add main dy dia 

                    else: # agar current_user_todo ky andar phaly sy task nhi howa do
                        new_todo : dict = {
                            "taskNo": 1,
                            "text": task, # is main user ka task aye ga
                            "addDate" : f"{datetime.now().strftime("%Y-%m-%d")}", # jab user new task add kar ry ga us din ki date aye gi,
                            "priority": priority, # is main llm jo select kar lyga wo is main aye ga
                            "completed": False
                        }
                        user_data["todoList"].append(new_todo) # is main user_data ky todoList main new task add kia
                        after_add.append(user_data) # is main current user ka pora data after_add main dy dia 

                else: # is main current user ky alawa sary user ka data after_add main jaye ga
                    after_add.append(user_data)


            with open("personal_information.json", "w") as file: # is main sary task personal_information.json main jarahe hai
                json.dump(after_add, file, indent=4)
            

            with open("personal_information.json", "r") as file:
                todo_list : list[dict] = json.load(file)
                filter_user = list(filter(lambda x : x["email"] == user_email and x["password"] == user_password, todo_list)) # is main current user ko filter kar raha ho
                
                if filter_user: # is check kar raha ho ky current user ka task add ho gaya ya nhi
                    current_user_todo = filter_user[0]["todoList"]
                    check = list(filter(lambda x : x["text"] == task, current_user_todo)) #is main check kar raha ho ky jo user ny task dia hai wo add ho gaya hai ya nhi

                    if check: # agar task add ho gaya ho ye chaly ga wana else
                        return True
                    else:
                        return False
                else:
                    return False
    


@function_tool
def remove_task(task_no: int) -> None: # is ky andar task number aye ga
    """
    # 🗑️ Remove Task from To-Do List

    Remove a task based on its task number (`task_no`).

    ### 📥 Input:
    - **task_no (int)**: The number of the task to remove from the list.

    ### 📌 Instructions for AI:
    - Is function ka use sirf tab karo jab user keh raha ho:
      - "Delete task 2"
      - "Remove task number 4"
      - "Delete my meeting task"
    - Tum task number identify karo aur usay is function mein do.
    - Task delete karne ke baad, remaining tasks ko dobara re-number karo from 1 onwards.

    ### ⚠️ Notes:
    - Agar task number exist nahi karta, toh user ko politely batao.
    """

    # is ky andar current_user_email_password.json sy current user ka email or password get kar raha ho
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai

        after_remove : list[dict] = [] # is main current user ka task remove hoky is main aye ga

        with open("personal_information.json", "r") as file:
            all_user : list[dict]= json.load(file)

            for user_data in all_user: # is main ek ek karky sary user is main aye gy
                if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho
                    user_todo = user_data["todoList"] # is main current user ka todo list aye ga

                    check = list(filter(lambda x: x["taskNo"] == task_no, user_todo)) # is main check kar raha ho ky jo user ny task number dia hai wo user_todo ky andar hai ya nhi

                    if check: # agar user wala taskNo user_todo main howa to ye chaly ga wana else 
                        new_todo_list = [task for task in user_todo if task["taskNo"] != task_no]  # Pehle task remove karo jo match karta hai
                        
                        # jo remaining tasks hai un ky phil sy taskNo generate ho rahy hai 
                        for idx, task in enumerate(new_todo_list, start=1):
                            task["taskNo"] = idx

                        # is main remove ny ky baat or remaining ky taskNo generate ho ny ky baat is main task aye gy 
                        user_data["todoList"] = new_todo_list

                        # remove ny ky baat current user ka data after_remove ky andar jaye ga
                        after_remove.append(user_data)
                    # agar check ky andar taskNO nhi mila to ye chaly ga
                    else:
                        return False
                else: # is main current user ky alawa sary user ka data after_remove main jaye ga
                    after_remove.append(user_data)

        with open("personal_information.json", "w") as file: # is main sary task personal_information.json main jarahe hai
            json.dump(after_remove, file, indent=4)
        
        return True



@function_tool
def complete_task(task_no : int) -> bool: # is main user ka task number aye ga
    """
    # ✅ Mark Task as Completed

    Complete a task in the to-do list based on its task number (`task_no`).

    ### 📥 Input:
    - ***task_no (int)***: The number of the task that should be marked as completed.

    ### 📌 Instructions for AI:
    - Jab user kahe:
      - "Mark task 3 as done"
      - "I completed task 5"
      - "Check off task 2"
    - Tum us task number ko identify karo aur is function mein do.
    - Sirf `completed` field ko `True` karo, baki data waise ka waise rahe.

    ### 📋 Example:
    - Input: `task_no = 2`
    - Output: Task with `taskNo: 2` will now have `"completed": true`

    ### ⚠️ Notes:
    - Agar task number nahi milta, to user ko politely inform karo ke "Task not found".
    """

    # is ky andar current_user_email_password.json sy current user ka email or password get kar raha ho
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai


        after_complete : list[dict] = [] # is main task complyte kar ny ky baat sary task is main aye gy

        with open("personal_information.json", "r") as file:
            all_user : list[dict] = json.load(file)
            
            for user_data in all_user: # is main ek ek karky sary user is main aye gy
                if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho
                    user_todo = user_data["todoList"] # is main current user ka todo list aye ga
                    check = list(filter(lambda x: x["taskNo"] == task_no, user_todo)) # is main check kar raha ho ky jo user ny task number dia hai wo user_todo ky andar hai ya nhi

                    if check: # agar user wala taskNo user_todo main howa to ye chaly ga wana else 
                        for todo in user_todo: 
                            if todo["taskNo"] == task_no: # jo user ny taskNo dia hai bas us ky task ky andar jo completed hai us ko True ho raha hai
                                todo["completed"] = True

                        # complete ho ny ky baat current user ka data after_complete ky andar jaye ga
                        after_complete.append(user_data) 
                    else: # agar check ky andar taskNO nhi mila to ye chaly ga
                        return False
                else: # is main current user ky alawa sary user ka data after_complete main jaye ga
                    after_complete.append(user_data)

        with open("personal_information.json", "w") as file: # is main sary task personal_information.json main jarahe hai
            json.dump(after_complete, file, indent=4)
        
        return True



@function_tool
def edit_task(task_no : int, task : str) -> bool: # is main user ka task number or new update task aye ga
    """
    # ✏️ Edit a Task in the To-Do List

    Update the text/description of a task based on its task number.

    ### 📥 Input:
    - ***task_no (int)***: Task number jisko update karna hai.
    - ***task (str)***: Naya task description jo update karna hai.

    ### 📌 Instructions for AI:
    - Jab user kahe:
      - "Change task 3 to 'Buy groceries'"
      - "Edit task 2 and make it 'Finish assignment'"
      - "Update task number 4"
    - Tum `task_no` aur `task` dono extract karo aur is function ko call karo.

    ### ✅ Behavior:
    - Sirf `text` field update karo, baaki fields (e.g., priority, completed) as-is rehne do.
    - Update ke baad JSON file dobara save karo.

    ### ⚠️ Note:
    - Agar `task_no` exist nahi karta, to user ko politely inform karo ke "Task not found".
    """

    # is ky andar current_user_email_password.json sy current user ka email or password get kar raha ho
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai


        after_edit : list[dict] = [] # is main task eidt kar ny ky baat sary task is main aye gy

        with open("personal_information.json", "r") as file:
            all_user : list[dict] = json.load(file)

            for user_data in all_user: # is main ek ek karky sary user is main aye gy
                if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho
                    user_todo = user_data["todoList"] # is main current user ka todo list aye ga

                    check = list(filter(lambda x: x["taskNo"] == task_no, user_todo)) # is main check kar raha ho ky jo user ny task number dia hai wo user_todo ky andar hai ya nhi

                    if check: # agar user wala taskNo user_todo main howa to ye chaly ga wana else 
                        for todo in user_todo:
                            if todo["taskNo"] == task_no: # jo user ny taskNo dia hai bas us ky text main update wala task add ho jaye ga
                                todo["text"] = task

                        # edi ho ny ky baat current user ka data after_edit ky andar jaye ga
                        after_edit.append(user_data)
                    else: # agar check ky andar taskNO nhi mila to ye chaly ga
                        return False
                else: # is main current user ky alawa sary user ka data after_edit main jaye ga
                    after_edit.append(user_data)

        with open("personal_information.json", "w") as file: # is main sary task personal_information.json main jarahe hai
            json.dump(after_edit, file, indent=4)
        
        return True


@function_tool
def read_todo_list() -> list[dict]: # is main user ky task user ko show ho ye ga
    """
    # 📄 Read Todo List

    - Yeh tool `personal_information.json` file se tamam tasks read karta hai aur list ki form mein return karta hai.
    - Har task ek dictionary hota hai jisme fields hote hain:
        - `taskNo` (int): Task ka unique number
        - `text` (str): Task ka description
        - `addDate` (str): Task kab add hua (format: YYYY-MM-DD)
        - `priority` (str): Task ki priority (jaise: low, medium, high, urgent, none)
        - `completed` (bool): Task complete hai ya nahi

    ## 🔍 Istemaal:
    Jab user kahe:
    - "Mujhe apni to-do list dikhao"
    - "Show me all tasks"
    - "Saare tasks list karo"

    To is tool ko use karo aur result mein list of tasks return karo.

    ## Note 
    user ko sahe format main todo list show karna user sahe sy understanding karry
    """

    # is ky andar current_user_email_password.json sy current user ka email or password get kar raha ho
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai

        with open("personal_information.json", "r") as file:
            all_user : list[dict] = json.load(file)

            for user_data in all_user: # is main ek ek karky sary user is main aye gy
                if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho
                    user_todo = user_data["todoList"] # is main current user ka todo list aye ga

                    return user_todo


 