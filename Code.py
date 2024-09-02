def get_int_input(prompt, allow_empty=False):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and allow_empty:
                return None
            value = int(user_input)
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_str_input(prompt, allow_empty=False):
    while True:
        user_input = input(prompt).strip()
        if not user_input and allow_empty:
            return None
        if user_input:
            return user_input
        else:
            print("Input cannot be empty. Please try again.")

def get_valid_phone_number(prompt):
    while True:
        phone_number = get_int_input(prompt)
        if phone_number and len(str(phone_number)) == 10:
            return phone_number
        else:
            print("Invalid phone number. Please enter a 10-digit phone number.")

def get_valid_email(prompt):
    while True:
        email = get_str_input(prompt)
        if "@" in email and "." in email:
            return email
        else:
            print("Invalid email format. Please enter a valid email address.")

print("#########################################################")
print("Welcome to the repository")
print()
print("What's the purpose of your visit")
print("1. Enter student's details")
print()
d = {}  # Empty dictionary to store details

ch = get_int_input("Enter your choice: ")

if ch == 1:
    n = get_int_input("Enter the number of students: ")
    for i in range(n):
        x = get_int_input("Enter student's roll number: ")
        a = get_str_input("Enter student's name: ")
        b = get_valid_phone_number("Enter student's mobile number: ")
        c = get_valid_email("Enter student's email: ")
        print("*************************************************************")
        d[x] = [a, b, c]  # Store the details in the dictionary

    print("Data Entered successfully!!!")
    print()
    print("#########################################################")
    print()
    print("Press 1 to search via roll number")
    cx = get_int_input("Enter your choice: ")  # Program for searching the desired roll number
    if cx == 1:
        j = get_int_input("Enter roll number to be searched: ")
        if j in d:
            print("Data found in the repository")
            print(d.get(j))  # Get the result
        else:
            print("No data found for the given roll number.")
    else:
        print("Enter valid choice")
else:
    print("Enter valid choice")

print()
print("Thank you for choosing this repository\nWe hope you liked our service")
