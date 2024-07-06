import json
import uuid
from datetime import datetime
from pathlib import Path

STORAGE_LOCATION = "storage.json"
operations = {
    "c": "create",
    "r": "read",
    "u": "update",
    "d": "delete",
    "x": "exit"
}

def initialize_storage():
    try:
        print("Initializing...")
        storage_init = {
            "todos": [],
            "date_created": datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
        }
        write_storage(storage_init)
        
    except:
        print("Failed to initialize storage!")

def read_storage():
    try:
        print("Accessing storage...")
        storage_location = Path(STORAGE_LOCATION)

        if not storage_location.is_file():
            print("Storage file not found!")
            initialize_storage()
            print("Storage created!")

        storage_file = open(STORAGE_LOCATION)
        storage_data = json.load(storage_file)  

        return storage_data  
    
    except:
        print("Error occurred while accessing storage!")
        return None

def write_storage(payload):
    try:
        data = json.dumps(
            obj = payload,
            indent = 4,
            default = str
        )

        with open(STORAGE_LOCATION, "w") as file_output:
            file_output.write(data)

    except:
        print("Failed to write to storage!")

def present_options():
    try:
        user_option = ""

        while user_option != "x":
            enabled_commands = []
            commands = list(operations.keys())
            statement = "What would you like to do?\n"
            storage_data = read_storage()
            todos_length = len(storage_data["todos"])

            for command in commands:
                if command != "c" and command != "x" and todos_length == 0:
                    continue
                else:
                    statement = statement + f" {command} ({operations[command]})\n"
                    enabled_commands.append(command)

            statement = statement + "enter: "
            user_option = input(statement)

            while user_option not in enabled_commands:
                print("Invalid option, try again.")
                user_option = present_options(todos_length)

            if user_option == "c":
                create_todo()
            if user_option == "r":
                read_todos()
            if user_option == "u":
                update_todo()
            if user_option == "d":
                delete_todo()
            if user_option == "x":
                print("Exiting...")

    except:
        print("Failed to present options!")

def create_todo():
    try:
        todo = input("Enter a new todo: ")
        todo_obj = {
            "id": uuid.uuid4().hex,
            "content": todo,
            "date_created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        storage_file = open(STORAGE_LOCATION)
        storage_data = json.load(storage_file) 
        storage_data["todos"].append(todo_obj)

        write_storage(storage_data)
        print("Todo created!")  

    except:
        print("Failed to create todo!")

def read_todos():
    try:
        storage_data = read_storage()

        if len(storage_data["todos"]) > 0:
            print("My todos:")
    
            for i, todo in enumerate(storage_data["todos"]):
                print(f" {i+1}. {todo["content"]}")

    except:
        print("Failed to read todos!") 

def update_todo():
    try:
        storage_data = read_storage()
        options = "Which todo to update? (type index value) \n"

        for i, todo in enumerate(storage_data["todos"]):
            options = options + f"{i+1}. {todo["content"]} \n"

        options = options + "enter: "
        user_option = int(input(options))
        num_of_todos = len(storage_data["todos"])

        while user_option > num_of_todos or user_option <= 0:
            print("Invalid selection, try again!")
            update_todo()
        
        selected_todo = storage_data["todos"][user_option - 1]

        print("Selected todo: " + selected_todo["content"])

        user_update = input("enter: ")
        selected_todo["content"] = user_update
        selected_todo["last_updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        write_storage(storage_data)
        print("Updated!")

    except:
        print("Failed to update todo!")

def delete_todo():
    try:
        storage_data = read_storage()
        options = "Which todo to delete? (type index value) \n"

        for i, todo in enumerate(storage_data["todos"]):
            options = options + f"{i+1}. {todo["content"]} \n"
        
        options = options + "enter: "
        user_option = int(input(options))
        num_of_todos = len(storage_data["todos"])

        while user_option > num_of_todos or user_option <= 0:
            print("Invalid selection, try again!")
            delete_todo()
        
        deleted_todo = storage_data["todos"].pop(user_option - 1)

        write_storage(storage_data)
        print("Deleted todo!: " + deleted_todo["content"])

    except:
        print("Failed to delete todo!")

if __name__ == "__main__":
    print("Welcome to Terminal Todo!")
    storage_data = read_storage()

    if storage_data:
        present_options()
    else:
        print("Unable to load data, exiting...")