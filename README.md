# Student Management System

## Overview

A comprehensive student management application with both command-line and graphical user interfaces. Manage student records including roll numbers, names, phone numbers, and email addresses with full CRUD operations and multiple search capabilities.

## Features

- Add new student records with validation
- Edit existing student information
- Search students by roll number, name, phone number, or email
- View all student records in a formatted table
- Data persistence using JSON storage
- Input validation for all fields
- Duplicate roll number prevention

## Requirements

- Python 3.x
- tkinter (included with standard Python installation)

## Installation

Clone the repository to your local machine:
```bash
git clone https://github.com/Hrk84ya/classmate-repository
cd classmate-repository
```

## Usage

### GUI Version (Recommended)

Run the graphical interface:
```bash
python GUI.py
```

The GUI provides an intuitive interface with buttons for all operations:
- Add Student: Enter new student details through a form
- Edit Student: Search by roll number and update information
- Search Student: Find students using multiple search criteria
- View All: Display all students in a scrollable table
- Exit: Close the application

### Command-Line Version

Run the terminal-based interface:
```bash
python Code.py
```

Menu options:
1. Enter student details: Add one or multiple students
2. Edit student details: Modify existing records by roll number
3. Search student data: Find students by roll number, name, phone, or email
4. Show all students data: Display complete student list
5. Exit: Save and close the application

## Data Storage

Student data is automatically saved to `student_data.json` in the project directory. The file is created automatically on first use and updated after each modification.

## Validation Rules

- Roll Number: Must be a unique integer
- Name: Letters, spaces, hyphens, and apostrophes only
- Phone Number: Exactly 10 digits
- Email: Valid email format (user@example.com)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (git checkout -b feature/new-feature)
3. Make your changes
4. Commit your changes (git commit -am 'Add new feature')
5. Push to the branch (git push origin feature/new-feature)
6. Create a new Pull Request

Please ensure your code adheres to the repository's coding standards and includes appropriate documentation.
