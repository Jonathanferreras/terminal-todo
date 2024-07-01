import json
from datetime import datetime
from pathlib import Path

STORAGE_LOCATION = "storage.json"

operations = {
    "c": "create",
    "u": "update",
    "d": "delete"
}

def read_storage():
    print("Accessing storage...")

    try:
        storage_location = Path(STORAGE_LOCATION)

        if not storage_location.is_file():
            print("Storage file not found, initializing...")
            
            storage_init = json.dumps(
                obj = {
                    "todos": [],
                    "date_created": datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
                },
                indent = 4,
                default = str
            )

            with open(STORAGE_LOCATION, "w") as file_output:
                file_output.write(storage_init)
                print("Storage created!")

        storage_file = open(STORAGE_LOCATION)
        storage_data = json.load(storage_file)   

        return storage_data  
    
    except:
        print("Error occurred while accessing storage!")
        return None

def present_options(todos_length):
    enabled_commands = []
    commands = list(operations.keys())
    statement = "What would you like to do? press "


    for command in commands:
        if command != "c" and todos_length == 0:
            continue
        else:
            statement = statement + f"{command} ({operations[command]}) "
            enabled_commands.append(command)

    user_option = input(statement)

    while user_option not in enabled_commands:
        print("Invalid option, try again.")
        user_option = present_options(todos_length)

    return user_option

    

if __name__ == "__main__":
    print("Welcome to Terminal Todo!")
    storage_data = read_storage()

    if storage_data:
        # logic here

        # TODO: implement while loop to have repeatable action
        todos_length = len(storage_data["todos"])
        user_option = present_options(todos_length)

        # TODO: perform action based on option chosen




    else:
        print("Unable to load data, exiting...")