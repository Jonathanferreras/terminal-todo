import json
from datetime import datetime
from pathlib import Path

STORAGE_LOCATION = "storage.json"

def read_storage():
    print("Accessing storage...")

    try:
        storage_location = Path(STORAGE_LOCATION)

        if not storage_location.is_file():
            print("Storage file not found, initializing...")
            
            storage_init = json.dumps(
                {
                    "todos": [],
                    "date_created": datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
                },
                indent=4,
                default=str
            )

            with open(STORAGE_LOCATION, "w") as file:
                file.write(storage_init)
                print("Storage created!")

        storage_file = open(STORAGE_LOCATION)
        storage_data = json.load(storage_file)   

        return storage_data  
    
    except:
        print("Error occurred while accessing storage!")
        return None



if __name__ == "__main__":
    print("Welcome to Terminal Todo!")
    storage_data = read_storage()

    # TODO: apply crud operations next