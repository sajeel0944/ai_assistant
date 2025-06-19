from agents import function_tool
import json
from datetime import datetime

@function_tool
def add_personal_information(dataType: str, information: str, priority: str) -> bool:
    """
    # Add Personal Information Function Prompt

    The purpose of this function is to allow the LLM to automatically identify and save specific personal information from a user's query without
    notifying the user. The LLM must intelligently select relevant information, categorize it with an appropriate dataType and priority, and store
    it in the personal_information.json file associated with the user's credentials

   The LLM will analyze the user's query or statement and automatically decide which information is worth saving as personal information. Examples of information to save include:
    - I like pizza in my meals
    - my account number is 3489758475
    - My NIC number is "7647677374"
    - I enjoy reading
    - I don’t like shopping
    - How much money is in my account?
    Beyond these examples, the LLM should automatically identify any other personal information in the user's query and decide whether to save it.

    ## Parameters

    ### dataType : str
        - The LLM will determine the appropriate `dataType` for the information being saved.
        - Based on the selected information from the user's query, the LLM will assign a `dataType`. Suggested categories include:
            - `preference`: For likes, dislikes, or hobbies (e.g., "I like pizza" → `dataType: "preference"`)
            - `personal_detail`: For identification details (e.g., "My NIC number is 7647677374" → `dataType: "personal_detail"`)
            - `financial`: For money-related information (e.g., "How much money is in my account?" → `dataType: "financial"`)
            - `other`: For any information that doesn’t fit the above categories

    ### information : str
        - This will contain the exact statement or relevant portion of the user's query that the LLM selects for saving.
        - Example: If the user says, "I like pizza and want to order some today," the LLM will extract `information: "I like pizza"`.

    ### priority : str
        - The LLM will determine the priority level of the information based on its importance or sensitivity.
        - Based on the selected information, the LLM will assign a priority. Suggested levels include:
            - `high`: For sensitive information (e.g., "My NIC number is 7647677374" → `priority: "high"`)
            - `medium`: For preferences or hobbies (e.g., "I like pizza" → `priority: "medium"`)
            - `low`: For less significant information (e.g., "I walked my dog today" → `priority: "low"`)

    # Note
    - After saving the user's information, the LLM must not inform the user that their information has been saved. The process should be completely transparent.
    - The LLM must ensure the information is correctly saved in `personal_information.json` with the user's credentials from `current_user_email_password.json`.
    - If the user's credentials are not found in `current_user_email_password.json` or if the JSON file is inaccessible or corrupted, the function should return `False`.
    - The function should return `True` if the information is successfully saved, otherwise `False`.
    - The `addDate` field must automatically include the current date in `YYYY-MM-DD` format (e.g., "2025-06-18").
    - Example Workflow:
        - Query: "My NIC number is 7647677374, and I like pizza."
        - LLM Actions:
            1. Identify: "My NIC number is 7647677374" and "I like pizza" as information to save.
            2. Assign:
                - For "My NIC number is 7647677374": `dataType: "personal_detail"`, `information: "My NIC number is 7647677374"`, `priority: "high"`
                - For "I like pizza": `dataType: "preference"`, `information: "I like pizza"`, `priority: "medium"`
            3. Save both entries with `addDate: "2025-06-18"` in `personal_information.json`.
            4. Return `True` if saved successfully, `False` otherwise.
    """

    # is ky andar current_user_email_password.json sy current user ka email or password get kar raha ho
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai

        after_add : list[dict] = [] # is main current user ki new information add ho ky is mian aye gi

        with open("personal_information.json" , "r") as file:
            all_user = json.load(file)

            for user_data in all_user: # is main ek ek karky sary user is main aye gy
                if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho

                    new_information : dict = {
                            "dataType": dataType,  # is main llm jo select kar lyga wo is main aye ga
                            "text": information, # is main user ki information aye ga
                            "addDate" : f"{datetime.now().strftime("%Y-%m-%d")}", # jab user new information add kar ry ga us din ki date aye gi,
                            "priority": priority, # is main llm jo select kar lyga wo is main aye ga
                        }
                    
                    user_data["userInformation"].append(new_information) # is main user_data ky andar jo userInformation hai us main new information add kia hai
                    after_add.append(user_data) # is main current user ka pora data after_add main dy dia 
                else:
                    after_add.append(user_data)


        with open("personal_information.json", "w") as file: # is main sary information personal_information.json main jarahe hai
           json.dump(after_add, file, indent=4)


        with open("personal_information.json", "r") as file:
                information_list : list[dict] = json.load(file)
                filter_user = list(filter(lambda x : x["email"] == user_email and x["password"] == user_password, information_list)) # is main current user ko filter kar raha ho
                
                if filter_user: # is check kar raha ho ky current user ki information add ho gaya ya nhi
                    current_user_information = filter_user[0]["userInformation"]
                    check = list(filter(lambda x : x["text"] == information, current_user_information)) #is main check kar raha ho ky jo user ny information dia hai wo add ho gaya hai ya nhi

                    if check: # agar task add ho gaya ho ye chaly ga wana else
                        return True
                    else:
                        return False
                else:
                    return False
                

@function_tool
def raed_specific_information(dataType: str = "", priority: str = "") -> dict | bool:
    """
    # Read Specific Information Function Prompt

    The purpose of this function is to allow the LLM to retrieve specific personal information from the personal_information.json file based 
    on either a dataType or priority parameter provided by the user's query. The LLM must select only one parameter (dataType or priority) to 
    filter the information, never both simultaneously, and return the matching information or False if no information is found.


   The LLM will analyze the user's query to determine whether to filter by `dataType` or `priority`. Examples of user queries include:
    - "Tell me what food I like to eat."
    - "What is my account number?"
    - "Do I like shopping?"

    The LLM will automatically decide which parameter (`dataType` or `priority`) to use and what value to assign based on the query.

    ## Parameters (Only one parameter will have a value at a time)

    ### dataType : str
        - The LLM will determine the appropriate `dataType` to filter information based on the user's query.
        - The LLM will read the query and select a `dataType` that matches the type of information requested. Suggested categories include:
            - `preference`: For queries about likes, dislikes, or hobbies (e.g., "Tell me what food I like" → `dataType: "preference"`)
            - `personal_detail`: For queries about identification details (e.g., "What is my account number?" → `dataType: "personal_detail"`)
            - `financial`: For queries about money-related information (e.g., "How much money is in my account?" → `dataType: "financial"`)
            - `other`: For queries that don’t fit the above categories
        - Example Queries and `dataType`:
            - "Tell me what food I like to eat" → `dataType: "preference"`
            - "What is my NIC number?" → `dataType: "personal_detail"`
            - "How much money is in my account?" → `dataType: "financial"`

    ### priority : str
        - The LLM will determine the appropriate `priority` to filter information based on the user's query.
        - The LLM will read the query and select a `priority` that matches the importance or sensitivity of the requested information. Suggested levels include:
            - `high`: For sensitive information like identification or financial details (e.g., "What is my account number?" → `priority: "high"`)
            - `medium`: For preferences or hobbies (e.g., "Tell me what food I like" → `priority: "medium"`)
            - `low`: For less significant information (e.g., "What did I do today?" → `priority: "low"`)
        - Example Queries and `priority`:
            - "What is my NIC number?" → `priority: "high"`
            - "Do I like shopping?" → `priority: "medium"`
            - "What did I do today?" → `priority: "low"`

    # Note
    - The LLM must choose to filter by either `dataType` or `priority`, never both, based on the context of the user's query.
    - If no matching information is found in `personal_information.json` for the specified `dataType` or `priority`, the function must return `False`.
    - If the user's credentials are not found in `current_user_email_password.json` or if the JSON file is inaccessible or corrupted, the function must return `False`.
    - The function returns a list of matching information (as dictionaries) if found, or `False` if no information matches the filter.
    - The LLM must not inform the user about the internal process of retrieving information.
    - Example Workflow:
        - Query: "Tell me what food I like to eat."
        - LLM Actions:
            1. Identify: The query is about preferences.
            2. Assign: `dataType: "preference"`, `priority: ""` (empty).
            3. Filter: Retrieve all entries from `personal_information.json` for the user where `dataType` is "preference".
            4. Return: A list of matching entries (e.g., `[{"dataType": "preference", "text": "I like pizza", "addDate": "2025-06-18", "priority": "medium"}]`) or `False` if none found.
        - Query: "What is my NIC number?"
        - LLM Actions:
            1. Identify: The query is about a personal detail.
            2. Assign: `dataType: "personal_detail"`, `priority: ""` (empty).
            3. Filter: Retrieve all entries where `dataType` is "personal_detail".
            4. Return: A list of matching entries (e.g., `[{"dataType": "personal_detail", "text": "My NIC number is 7647677374", "addDate": "2025-06-18", "priority": "high"}]`) or `False` if none found.
    """
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai

        with open("personal_information.json" , "r") as file:
            all_user = json.load(file)

        for user_data in all_user: # is main ek ek karky sary user is main aye gy
                if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho
                    user_information = user_data["userInformation"] # is main current user ka information list aye gi
                    
                    if dataType:
                        filter_datatype_information =list(filter(lambda x : x["dataType"].lower() == dataType.lower(), user_information) )
                        if filter_datatype_information:
                            return filter_datatype_information
                        else:
                            return False
                    
                    elif priority:
                        filter_priority_information =list(filter(lambda x : x["priority"].lower() == priority.lower(), user_information))
                        if filter_priority_information:
                            return filter_priority_information
                        else:
                            return False
                        

@function_tool
def show_all_information() -> list[dict]:
    """
    # Show All Information Function Prompt

    The purpose of this function is to retrieve all personal information stored for the current user from the personal_information.json file. 
    The LLM will use the user's credentials from current_user_email_password.json to filter and return the complete list of the user's stored 
    information.

    The function will return all information associated with the current user, including all entries previously saved (e.g., preferences, 
    personal details, financial information) as a list of dictionaries.

    ## Parameters
    - This function takes **no parameters** as it is designed to retrieve all information for the authenticated user without any filtering.

    ## Functionality
    - The LLM will:
        1. Show the current user's email and password from `current_user_email_password.json`.
        2. Access the `personal_information.json` file and filter the data to find the user matching the provided email and password.
        3. Return the entire `userInformation` list for that user, which contains all stored entries in the format:
            ```json
            {
                "dataType": "<type_of_information>",
                "text": "<stored_information>",
                "addDate": "<date_in_YYYY-MM-DD_format>",
                "priority": "<priority_level>"
            }
            ```
        4. If no matching user is found or if the JSON files are inaccessible or corrupted, the function should return an empty list (`[]`).

    ## Example Workflow
    - **Scenario**: The user’s credentials are `email: "user@example.com"`, `password: "secure123"`, and `personal_information.json` contains:
        ```json
        [
            {
                "email": "user@example.com",
                "password": "secure123",
                "userInformation": [
                    {"dataType": "preference", "text": "I like pizza", "addDate": "2025-06-18", "priority": "medium"},
                    {"dataType": "personal_detail", "text": "My NIC number is 7647677374", "addDate": "2025-06-18", "priority": "high"}
                ]
            },
            {
                "email": "other@example.com",
                "password": "pass456",
                "userInformation": [...]
            }
        ]
        ```
    - **LLM Actions**:
        1. show credentials from `current_user_email_password.json`: `email: "user@example.com"`, `password: "secure123"`.
        2. Filter `personal_information.json` to find the user with matching email and password.
        3. Retrieve the `userInformation` list for the matching user.
        4. Return:
            ```json
            [
                {"dataType": "preference", "text": "I like pizza", "addDate": "2025-06-18", "priority": "medium"},
                {"dataType": "personal_detail", "text": "My NIC number is 7647677374", "addDate": "2025-06-18", "priority": "high"}
            ]
            ```
    - **Error Case**: If no user matches the credentials or the JSON files are inaccessible, return `[]`.

    # Note
    - The LLM must not inform the user about the internal process of retrieving information.
    - The function assumes that `personal_information.json` contains a list of user objects, each with an `email`, `password`, and `userInformation` field.
    - The function must handle errors gracefully, returning an empty list (`[]`) if:
        - The user’s credentials are not found in `current_user_email_password.json`.
        - The `personal_information.json` file is inaccessible or corrupted.
        - No matching user is found in `personal_information.json`.
    - The returned list will include all entries in the `userInformation` field, regardless of `dataType` or `priority`.
    """
    with open("current_user_email_password.json", "r") as file:
        email_and_password = json.load(file)
        user_email = email_and_password["email"] # is main email arahe hai
        user_password = email_and_password["password"] #  is main password araha hai

    with open("personal_information.json" , "r") as file:
        all_user = json.load(file)

        for user_data in all_user: # is main ek ek karky sary user is main aye gy
            if user_data["email"] == user_email and user_data["password"] == user_password: # is main current user ko filter kar raha ho
                user_information = user_data["userInformation"] # is main current user ka information list aye gi
                return user_information  


 