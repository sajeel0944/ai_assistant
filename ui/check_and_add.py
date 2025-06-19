from dataclasses import dataclass
import json
from datetime import datetime 

@dataclass
class AddUser():
    email: str
    password: str
    fristName: str = ""
    lastName: str = ""


    def check_user(self) -> bool:
        with open("personal_information.json", "r") as file:
            data : list[dict] = json.load(file)
            check = list(filter(lambda x: x["email"] == self.email and x["password"] == self.password, data))
            
            if check:
                return True
            else:
                return False
            

    def add_user(self) -> bool:
        new_data : list[dict] = []

        schema : dict =  {
            "fristName": self.fristName,
            "lastName": self.lastName,
            "email": self.email,
            "password": self.password,
            "registerDate" : f"{datetime.now().strftime("%Y-%m-%d")}", # jab user register hoye ga is din ki date aye gi,
            "todoList": [],
            "userInformation" :[]
        }

        with open("personal_information.json", "r") as file:
            data : list[dict] = json.load(file)
            for i in data:
                new_data.append(i)
        
        new_data.append(schema)

        with open("personal_information.json", "w") as file:
            json.dump(new_data, file, indent=4)

        with open("personal_information.json", "r") as file:
            data : list[dict] = json.load(file)
            check = list(filter(lambda x: x["email"] == self.email and x["password"] == self.password, data))

            if check:
                return True
            else:
                return False
            

    def after_addcheck(self):
        schema = {
            "email" : self.email,
            "password" : self.password,
        }
        with open("current_user_email_password.json", "w") as file:
            json.dump(schema, file, indent=4)
            
             