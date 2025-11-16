import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import re

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.student_data = self.load_data_from_file()
        
        self.setup_ui()
    
    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg="#1a5490", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Student Management System", 
                              font=("Arial", 24, "bold"), bg="#1a5490", fg="white")
        title_label.pack(pady=20)
        
        button_frame = tk.Frame(self.root, bg="#f0f0f0", height=80)
        button_frame.pack(fill=tk.X, pady=10)
        
        btn_style = {"font": ("Arial", 11, "bold"), "width": 15, "height": 2, "bg": "#0066cc", "fg": "white", 
                     "relief": tk.RAISED, "bd": 3, "activebackground": "#0052a3", "activeforeground": "white", "cursor": "hand2"}
        
        tk.Button(button_frame, text="Add Student", command=self.show_add_student, **btn_style).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Edit Student", command=self.show_edit_student, **btn_style).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Search Student", command=self.show_search_student, **btn_style).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="View All", command=self.show_all_students, **btn_style).pack(side=tk.LEFT, padx=10)
        
        exit_style = btn_style.copy()
        exit_style["bg"] = "#cc0000"
        exit_style["activebackground"] = "#990000"
        tk.Button(button_frame, text="Exit", command=self.root.quit, **exit_style).pack(side=tk.LEFT, padx=10)
        
        self.content_frame = tk.Frame(self.root, bg="#ffffff")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.show_welcome()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_welcome(self):
        self.clear_content()
        welcome_label = tk.Label(self.content_frame, text="Welcome to Student Management System", 
                                font=("Arial", 18, "bold"), bg="#ffffff", fg="#000000")
        welcome_label.pack(pady=100)
        
        info_label = tk.Label(self.content_frame, text="Select an option from the menu above to get started", 
                             font=("Arial", 12), bg="#ffffff", fg="#333333")
        info_label.pack()
    
    def show_add_student(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Add New Student", font=("Arial", 16, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame, bg="#ffffff")
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Roll Number:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.roll_entry = tk.Entry(form_frame, font=("Arial", 11), width=30, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.roll_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Name:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 11), width=30, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.name_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Phone Number:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        self.phone_entry = tk.Entry(form_frame, font=("Arial", 11), width=30, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.phone_entry.grid(row=2, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Email:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=3, column=0, sticky=tk.W, pady=10, padx=10)
        self.email_entry = tk.Entry(form_frame, font=("Arial", 11), width=30, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.email_entry.grid(row=3, column=1, pady=10, padx=10)
        
        tk.Button(self.content_frame, text="Add Student", command=self.add_student, 
                 font=("Arial", 12, "bold"), bg="#009900", fg="white", width=20, height=2, 
                 activebackground="#007700", activeforeground="white", cursor="hand2", relief=tk.RAISED, bd=3).pack(pady=20)
    
    def add_student(self):
        roll_number = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not roll_number or not name or not phone or not email:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not roll_number.isdigit():
            messagebox.showerror("Error", "Roll number must be a valid integer")
            return
        
        if roll_number in self.student_data:
            messagebox.showerror("Error", "A student with this roll number already exists")
            return
        
        if not self.is_valid_name(name):
            messagebox.showerror("Error", "Invalid name. Only letters, spaces, hyphens, and apostrophes are allowed")
            return
        
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits")
            return
        
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        self.student_data[roll_number] = {
            'name': name.title(),
            'phone_number': phone,
            'email': email.lower()
        }
        
        self.save_data_to_file()
        messagebox.showinfo("Success", "Student added successfully")
        
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
    
    def show_edit_student(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Edit Student", font=("Arial", 16, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg="#ffffff")
        search_frame.pack(pady=20)
        
        tk.Label(search_frame, text="Enter Roll Number:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").pack(side=tk.LEFT, padx=10)
        self.edit_roll_entry = tk.Entry(search_frame, font=("Arial", 11), width=20, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.edit_roll_entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(search_frame, text="Search", command=self.load_student_for_edit, 
                 font=("Arial", 11, "bold"), bg="#0066cc", fg="white", activebackground="#0052a3", 
                 activeforeground="white", cursor="hand2", relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=10)
        
        self.edit_form_frame = tk.Frame(self.content_frame, bg="#ffffff")
        self.edit_form_frame.pack(pady=20)
    
    def load_student_for_edit(self):
        for widget in self.edit_form_frame.winfo_children():
            widget.destroy()
        
        roll_number = self.edit_roll_entry.get().strip()
        
        if not roll_number:
            messagebox.showerror("Error", "Please enter a roll number")
            return
        
        if roll_number not in self.student_data:
            messagebox.showerror("Error", "No student found with that roll number")
            return
        
        student = self.student_data[roll_number]
        
        tk.Label(self.edit_form_frame, text="Name:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        self.edit_name_entry = tk.Entry(self.edit_form_frame, font=("Arial", 11), width=30, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.edit_name_entry.insert(0, student['name'])
        self.edit_name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(self.edit_form_frame, text="Phone Number:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.edit_phone_entry = tk.Entry(self.edit_form_frame, font=("Arial", 11), width=30, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.edit_phone_entry.insert(0, student['phone_number'])
        self.edit_phone_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(self.edit_form_frame, text="Email:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=2, column=0, sticky=tk.W, pady=10, padx=10)
        self.edit_email_entry = tk.Entry(self.edit_form_frame, font=("Arial", 11), width=30, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.edit_email_entry.insert(0, student['email'])
        self.edit_email_entry.grid(row=2, column=1, pady=10, padx=10)
        
        tk.Button(self.edit_form_frame, text="Update Student", command=lambda: self.update_student(roll_number), 
                 font=("Arial", 12, "bold"), bg="#009900", fg="white", width=20, height=2,
                 activebackground="#007700", activeforeground="white", cursor="hand2", relief=tk.RAISED, bd=3).grid(row=3, column=0, columnspan=2, pady=20)
    
    def update_student(self, roll_number):
        name = self.edit_name_entry.get().strip()
        phone = self.edit_phone_entry.get().strip()
        email = self.edit_email_entry.get().strip()
        
        if not name or not phone or not email:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not self.is_valid_name(name):
            messagebox.showerror("Error", "Invalid name. Only letters, spaces, hyphens, and apostrophes are allowed")
            return
        
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits")
            return
        
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        self.student_data[roll_number] = {
            'name': name.title(),
            'phone_number': phone,
            'email': email.lower()
        }
        
        self.save_data_to_file()
        messagebox.showinfo("Success", "Student updated successfully")
        self.show_edit_student()
    
    def show_search_student(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="Search Student", font=("Arial", 16, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg="#ffffff")
        search_frame.pack(pady=20)
        
        tk.Label(search_frame, text="Search By:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        
        self.search_type = tk.StringVar(value="roll")
        tk.Radiobutton(search_frame, text="Roll Number", variable=self.search_type, value="roll", 
                      font=("Arial", 10, "bold"), bg="#ffffff", fg="#000000", selectcolor="#ffffff", 
                      activebackground="#ffffff", activeforeground="#000000").grid(row=0, column=1, sticky=tk.W, padx=5)
        tk.Radiobutton(search_frame, text="Name", variable=self.search_type, value="name", 
                      font=("Arial", 10, "bold"), bg="#ffffff", fg="#000000", selectcolor="#ffffff",
                      activebackground="#ffffff", activeforeground="#000000").grid(row=0, column=2, sticky=tk.W, padx=5)
        tk.Radiobutton(search_frame, text="Phone", variable=self.search_type, value="phone", 
                      font=("Arial", 10, "bold"), bg="#ffffff", fg="#000000", selectcolor="#ffffff",
                      activebackground="#ffffff", activeforeground="#000000").grid(row=0, column=3, sticky=tk.W, padx=5)
        tk.Radiobutton(search_frame, text="Email", variable=self.search_type, value="email", 
                      font=("Arial", 10, "bold"), bg="#ffffff", fg="#000000", selectcolor="#ffffff",
                      activebackground="#ffffff", activeforeground="#000000").grid(row=0, column=4, sticky=tk.W, padx=5)
        
        tk.Label(search_frame, text="Search Value:", font=("Arial", 11, "bold"), bg="#ffffff", fg="#000000").grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11), width=40, bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        self.search_entry.grid(row=1, column=1, columnspan=4, pady=10, padx=10)
        
        tk.Button(search_frame, text="Search", command=self.search_student, 
                 font=("Arial", 11, "bold"), bg="#0066cc", fg="white", width=15,
                 activebackground="#0052a3", activeforeground="white", cursor="hand2", relief=tk.RAISED, bd=3).grid(row=2, column=0, columnspan=5, pady=10)
        
        self.search_result_frame = tk.Frame(self.content_frame, bg="#ffffff")
        self.search_result_frame.pack(pady=20, fill=tk.BOTH, expand=True)
    
    def search_student(self):
        for widget in self.search_result_frame.winfo_children():
            widget.destroy()
        
        search_value = self.search_entry.get().strip()
        search_type = self.search_type.get()
        
        if not search_value:
            messagebox.showerror("Error", "Please enter a search value")
            return
        
        results = []
        
        if search_type == "roll":
            if search_value in self.student_data:
                results.append((search_value, self.student_data[search_value]))
        elif search_type == "name":
            for roll, student in self.student_data.items():
                if student['name'].lower() == search_value.lower():
                    results.append((roll, student))
        elif search_type == "phone":
            for roll, student in self.student_data.items():
                if student['phone_number'] == search_value:
                    results.append((roll, student))
        elif search_type == "email":
            for roll, student in self.student_data.items():
                if student['email'].lower() == search_value.lower():
                    results.append((roll, student))
        
        if results:
            result_text = scrolledtext.ScrolledText(self.search_result_frame, font=("Courier", 10), height=15, width=80,
                                                    bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
            result_text.pack(pady=10)
            
            result_text.insert(tk.END, f"{'Roll Number':<15} {'Name':<20} {'Phone':<15} {'Email':<30}\n")
            result_text.insert(tk.END, "=" * 80 + "\n")
            
            for roll, student in results:
                result_text.insert(tk.END, f"{roll:<15} {student['name']:<20} {student['phone_number']:<15} {student['email']:<30}\n")
            
            result_text.config(state=tk.DISABLED)
        else:
            tk.Label(self.search_result_frame, text="No student found", font=("Arial", 12, "bold"), bg="#ffffff", fg="#cc0000").pack(pady=20)
    
    def show_all_students(self):
        self.clear_content()
        
        tk.Label(self.content_frame, text="All Students", font=("Arial", 16, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
        
        if not self.student_data:
            tk.Label(self.content_frame, text="No student data available", font=("Arial", 12, "bold"), bg="#ffffff", fg="#cc0000").pack(pady=20)
            return
        
        result_text = scrolledtext.ScrolledText(self.content_frame, font=("Courier", 10), height=20, width=90,
                                                bg="#ffffff", fg="#000000", relief=tk.SOLID, bd=2)
        result_text.pack(pady=10, padx=10)
        
        result_text.insert(tk.END, f"{'Roll Number':<15} {'Name':<20} {'Phone':<15} {'Email':<30}\n")
        result_text.insert(tk.END, "=" * 80 + "\n")
        
        for roll, student in self.student_data.items():
            result_text.insert(tk.END, f"{roll:<15} {student['name']:<20} {student['phone_number']:<15} {student['email']:<30}\n")
        
        result_text.config(state=tk.DISABLED)
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_valid_name(self, name):
        pattern = r'^[A-Za-z\s\'-]+$'
        return re.match(pattern, name) is not None
    
    def save_data_to_file(self, filename="student_data.json"):
        with open(filename, "w") as file:
            json.dump(self.student_data, file, indent=2)
    
    def load_data_from_file(self, filename="student_data.json"):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
