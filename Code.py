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
        phone_number = get_str_input(prompt)
        if phone_number.isdigit() and len(phone_number) == 10:
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

def display_welcome():
    print("#########################################################")
    print("                      Welcome to the Repository")
    print("#########################################################")

def display_menu():
    print("\nWhat's the purpose of your visit?")
    print("1. Enter student details")
    print("2. Exit")

def display_search_menu():
    print("\n1. Search via roll number")
    print("2. Exit")

def main():
    display_welcome()
    display_menu()

    choice = get_int_input("\nEnter your choice: ")

    if choice == 1:
        student_data = {}  # Dictionary to store student details

        num_students = get_int_input("Enter the number of students: ")
        for i in range(num_students):
            roll_number = get_int_input("Enter student's roll number: ")
            name = get_str_input("Enter student's name: ")
            phone_number = get_valid_phone_number("Enter student's mobile number: ")
            email = get_valid_email("Enter student's email: ")
            student_data[roll_number] = [name, phone_number, email]
            print("\nStudent data entered successfully!")

        print("\nStudent data entry complete.\n")
        display_search_menu()

        search_choice = get_int_input("Enter your choice: ")
        if search_choice == 1:
            roll_number_to_search = get_int_input("Enter roll number to be searched: ")
            if roll_number_to_search in student_data:
                print("\nData found in the repository:")
                student_info = student_data.get(roll_number_to_search)
                print(f"Name: {student_info[0]}")
                print(f"Phone Number: {student_info[1]}")
                print(f"Email: {student_info[2]}")
            else:
                print("No data found for the given roll number.")
        else:
            print("Invalid choice. Exiting...")
    else:
        print("Invalid choice. Exiting...")

    print("\nThank you for using the repository. We hope you liked our service!")

if __name__ == "__main__":
    main()
