import json
import re

def get_int_input(prompt, allow_empty=False):
    """Function to get a valid integer input from the user."""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and allow_empty:
                return None
            value = int(user_input)
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_str_input(prompt, allow_empty=False, is_name=False):
    """Function to get a non-empty string input from the user."""
    while True:
        user_input = input(prompt).strip()
        if not user_input and allow_empty:
            return None
        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue
        if is_name and not is_valid_name(user_input):
            print("Invalid name. Only letters, spaces, hyphens, and apostrophes are allowed.")
            continue
        return user_input.title() if is_name else user_input

def get_valid_phone_number(prompt, allow_empty=False):
    """Function to get a valid 10-digit phone number from the user."""
    while True:
        phone_number = get_str_input(prompt, allow_empty)
        if phone_number.isdigit() and len(phone_number) == 10:
            return phone_number
        elif allow_empty and not phone_number:
            return None
        else:
            print("Invalid phone number. Please enter a 10-digit phone number.")

def is_valid_email(email):
    """Helper function to validate email using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_name(name):
    """Helper function to validate name (only letters, spaces, hyphens, and apostrophes)."""
    pattern = r'^[A-Za-z\s\'-]+$'
    return re.match(pattern, name) is not None

def get_valid_email(prompt, allow_empty=False):
    """Function to get a valid email address from the user."""
    while True:
        email = get_str_input(prompt, allow_empty)
        if allow_empty and not email:
            return None
        if is_valid_email(email):
            return email.lower()  # Store emails in lowercase for consistency
        print("Invalid email format. Please enter a valid email address (e.g., user@example.com)")

def display_welcome():
    """Function to display the welcome message."""
    print("#########################################################")
    print("                     Welcome to the Repository")
    print("#########################################################")

def display_menu():
    """Function to display the main menu."""
    print("\nWhat's the purpose of your visit?")
    print("1. Enter student details")
    print("2. Edit student details")
    print("3. Search student data")
    print("4. Show all students data")
    print("5. Exit")

def display_extended_search_menu():
    """Function to display the extended search menu."""
    print("\nSearch options:")
    print("1. Search via roll number")
    print("2. Search via name")
    print("3. Search via phone number")
    print("4. Search via email")
    print("5. Exit")

def display_student_info(student_info):
    """Helper function to display student information."""
    print(f"Name: {student_info['name']}")
    print(f"Phone Number: {student_info['phone_number']}")
    print(f"Email: {student_info['email']}")

def search_student_data(student_data):
    """Function to search student data by various attributes."""
    while True:
        display_extended_search_menu()
        search_choice = get_int_input("Enter your choice: ")

        if search_choice == 1:
            roll_number = get_int_input("Enter roll number to search: ")
            student_info = student_data.get(roll_number)
            if student_info:
                print("\nData found in the repository:")
                display_student_info(student_info)
            else:
                print("No student found with that roll number.")
        
        elif search_choice == 2:
            name = get_str_input("Enter name to search: ")
            found = False
            for student_info in student_data.values():
                if student_info['name'].lower() == name.lower():
                    print("\nData found in the repository:")
                    display_student_info(student_info)
                    found = True
            if not found:
                print("No student found with that name.")
        
        elif search_choice == 3:
            phone_number = get_valid_phone_number("Enter phone number to search: ")
            found = False
            for student_info in student_data.values():
                if student_info['phone_number'] == phone_number:
                    print("\nData found in the repository:")
                    display_student_info(student_info)
                    found = True
            if not found:
                print("No student found with that phone number.")
        
        elif search_choice == 4:
            email = get_valid_email("Enter email to search: ")
            found = False
            for student_info in student_data.values():
                if student_info['email'].lower() == email.lower():
                    print("\nData found in the repository:")
                    display_student_info(student_info)
                    found = True
            if not found:
                print("No student found with that email.")
        
        elif search_choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

def show_all_students_data(student_data):
    """Function to display all students' data in a custom tabular format."""
    if student_data:
        print("\nAll Students Data:")
        print("{:<15} {:<20} {:<15} {:<30}".format("Roll Number", "Name", "Phone Number", "Email"))
        print("=" * 80)
        for roll_number, details in student_data.items():
            print("{:<15} {:<20} {:<15} {:<30}".format(
                roll_number, details['name'], details['phone_number'], details['email']
            ))
    else:
        print("No student data available.")

def save_data_to_file(data, filename="student_data.json"):
    """Function to save student data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file)

def load_data_from_file(filename="student_data.json"):
    """Function to load student data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No previous data found. Starting fresh.")
        return {}
    except json.JSONDecodeError:
        print("Data file corrupted. Starting fresh.")
        return {}

def edit_student_data(student_data, roll_number):
    """Function to edit student details."""
    if roll_number in student_data:
        print(f"Editing data for student with roll number: {roll_number}")
        name = get_str_input("Enter new name (or press Enter to keep current): ", allow_empty=True, is_name=True)
        phone_number = get_valid_phone_number("Enter new phone number (or press Enter to keep current): ", allow_empty=True)
        email = get_valid_email("Enter new email (or press Enter to keep current): ", allow_empty=True)

        if name:
            student_data[roll_number]['name'] = name
        if phone_number:
            student_data[roll_number]['phone_number'] = phone_number
        if email:
            student_data[roll_number]['email'] = email
        
        print("Student data updated successfully!")
    else:
        print("No student found with that roll number.")

def main():
    """Main function to handle the overall flow of the repository."""
    display_welcome()

    student_data = load_data_from_file()

    while True:
        display_menu()
        choice = get_int_input("\nEnter your choice: ")

        if choice == 1:
            num_students = get_int_input("Enter the number of students: ")
            for i in range(num_students):
                print(f"\nEntering details for student {i+1}:")
                
                while True:
                    roll_number = get_int_input("Enter student's roll number: ")
                    if str(roll_number) in student_data:
                        print("Error: A student with this roll number already exists.")
                        print("Please enter a different roll number.")
                    else:
                        break
                        
                name = get_str_input("Enter student's name: ", is_name=True)
                phone_number = get_valid_phone_number("Enter student's mobile number: ")
                email = get_valid_email("Enter student's email: ")

                student_data[str(roll_number)] = {
                    'name': name,
                    'phone_number': phone_number,
                    'email': email
                }

                print("\nStudent data entered successfully!")

            save_data_to_file(student_data)  # Save the student data after entry

        elif choice == 2:
            roll_number = get_int_input("Enter the roll number of the student to edit: ")
            edit_student_data(student_data, roll_number)
            save_data_to_file(student_data)  # Save the updated data

        elif choice == 3:
            search_student_data(student_data)

        elif choice == 4:
            show_all_students_data(student_data)

        elif choice == 5:
            print("\nExiting the repository. Thank you for using our service!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
