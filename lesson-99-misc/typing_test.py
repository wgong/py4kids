from typing import Dict

def get_first_name(full_name: str) -> str:
    return full_name.split(" ")[0]

fallback_name: Dict[str, str] = {
    "first_name": "UserFirstName",
    "last_name": "UserLastName"
}

raw_name: str = input("Please enter your name: ")
first_name: str = get_first_name(raw_name)

# If the user didn't type anything in, use the fallback name
if not first_name:
    first_name = get_first_name(fallback_name)

print(f"Hi, {first_name}!")
