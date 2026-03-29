import tkinter as tk
from tkinter import ttk
import json
import re


class StudentManagementSystem:
    # Color palette
    BG = "#f0f2f5"
    SIDEBAR_BG = "#1e293b"
    SIDEBAR_HOVER = "#334155"
    SIDEBAR_ACTIVE = "#3b82f6"
    CARD_BG = "#ffffff"
    PRIMARY = "#3b82f6"
    PRIMARY_HOVER = "#2563eb"
    DANGER = "#ef4444"
    DANGER_HOVER = "#dc2626"
    SUCCESS = "#10b981"
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    TEXT_ON_DARK = "#e2e8f0"
    TEXT_ON_PRIMARY = "#ffffff"
    BORDER = "#e2e8f0"
    INPUT_BG = "#f8fafc"
    INPUT_FOCUS = "#3b82f6"
    TABLE_HEADER_BG = "#f1f5f9"
    TABLE_STRIPE = "#f8fafc"

    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)
        self.root.configure(bg=self.BG)

        self.student_data = self.load_data_from_file()
        self.active_btn = None
        self.ROWS_PER_PAGE = 10
        self._current_page = 0
        self._current_table_data = []

        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.SIDEBAR_BG, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Logo area
        logo_frame = tk.Frame(self.sidebar, bg=self.SIDEBAR_BG)
        logo_frame.pack(fill=tk.X, pady=(25, 30), padx=20)

        tk.Label(logo_frame, text="📚", font=("Arial", 28), bg=self.SIDEBAR_BG).pack()
        tk.Label(logo_frame, text="Student MS", font=("Helvetica", 16, "bold"),
                 bg=self.SIDEBAR_BG, fg=self.TEXT_ON_PRIMARY).pack(pady=(5, 0))
        tk.Label(logo_frame, text="Management System", font=("Helvetica", 9),
                 bg=self.SIDEBAR_BG, fg=self.TEXT_SECONDARY).pack()

        # Separator
        tk.Frame(self.sidebar, bg=self.SIDEBAR_HOVER, height=1).pack(fill=tk.X, padx=20, pady=(0, 15))

        # Nav buttons
        nav_items = [
            ("  🏠  Dashboard", self.show_welcome),
            ("  ➕  Add Student", self.show_add_student),
            ("  ✏️  Edit Student", self.show_edit_student),
            ("  🔍  Search", self.show_search_student),
            ("  📋  View All", self.show_all_students),
        ]

        self.nav_buttons = []
        for idx, (text, command) in enumerate(nav_items):
            btn_frame = tk.Frame(self.sidebar, bg=self.SIDEBAR_BG)
            btn_frame.pack(fill=tk.X)

            btn = tk.Label(btn_frame, text=text, font=("Helvetica", 12),
                           bg=self.SIDEBAR_BG, fg=self.TEXT_ON_DARK,
                           anchor="w", padx=20, pady=12, cursor="hand2")
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Add badge to "View All" nav item
            if idx == 4:
                count = len(self.student_data)
                self._badge_label = tk.Label(btn_frame, text=str(count) if count < 1000 else "999+",
                                             font=("Helvetica", 9, "bold"), bg=self.SIDEBAR_ACTIVE,
                                             fg="white", padx=6, pady=1)
                self._badge_label.pack(side=tk.RIGHT, padx=(0, 15))
                self._badge_label.bind("<Button-1>", lambda e, b=btn, c=command: self._on_nav_click(b, c))

            btn.bind("<Enter>", lambda e, b=btn, f=btn_frame: self._on_nav_hover(b, True, f))
            btn.bind("<Leave>", lambda e, b=btn, f=btn_frame: self._on_nav_hover(b, False, f))
            btn.bind("<Button-1>", lambda e, b=btn, c=command: self._on_nav_click(b, c))
            btn._parent_frame = btn_frame
            self.nav_buttons.append(btn)

        # Exit at bottom
        exit_frame = tk.Frame(self.sidebar, bg=self.SIDEBAR_BG)
        exit_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        tk.Frame(exit_frame, bg=self.SIDEBAR_HOVER, height=1).pack(fill=tk.X, padx=20, pady=(0, 10))
        exit_btn = tk.Label(exit_frame, text="  🚪  Exit", font=("Helvetica", 12),
                            bg=self.SIDEBAR_BG, fg=self.DANGER, anchor="w", padx=20, pady=12, cursor="hand2")
        exit_btn.pack(fill=tk.X)
        exit_btn.bind("<Enter>", lambda e: exit_btn.configure(bg=self.SIDEBAR_HOVER))
        exit_btn.bind("<Leave>", lambda e: exit_btn.configure(bg=self.SIDEBAR_BG))
        exit_btn.bind("<Button-1>", lambda e: self.root.quit())

        # Main content area
        self.main_area = tk.Frame(self.root, bg=self.BG)
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Content frame inside main area with padding
        self.content_frame = tk.Frame(self.main_area, bg=self.BG)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        # Show dashboard by default
        self._on_nav_click(self.nav_buttons[0], self.show_welcome)

    # --- Navigation helpers ---
    def _on_nav_hover(self, btn, entering, frame=None):
        if btn == self.active_btn:
            return
        bg = self.SIDEBAR_HOVER if entering else self.SIDEBAR_BG
        btn.configure(bg=bg)
        if frame:
            frame.configure(bg=bg)

    def _on_nav_click(self, btn, command):
        if self.active_btn:
            self.active_btn.configure(bg=self.SIDEBAR_BG, fg=self.TEXT_ON_DARK)
            if hasattr(self.active_btn, '_parent_frame'):
                self.active_btn._parent_frame.configure(bg=self.SIDEBAR_BG)
        btn.configure(bg=self.SIDEBAR_ACTIVE, fg=self.TEXT_ON_PRIMARY)
        if hasattr(btn, '_parent_frame'):
            btn._parent_frame.configure(bg=self.SIDEBAR_ACTIVE)
        self.active_btn = btn
        command()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- Toast notifications ---
    def _show_toast(self, message, toast_type="success"):
        """Show a non-blocking toast notification that auto-dismisses."""
        colors = {
            "success": ("#10b981", "#065f46", "✓"),
            "error": ("#ef4444", "#7f1d1d", "✕"),
            "info": ("#3b82f6", "#1e3a5f", "ℹ"),
        }
        bg, fg_dark, icon = colors.get(toast_type, colors["info"])

        toast = tk.Frame(self.root, bg=bg, highlightbackground=bg, highlightthickness=0)
        toast.place(relx=1.0, y=15, anchor="ne", x=-15)

        inner = tk.Frame(toast, bg=bg)
        inner.pack(padx=16, pady=10)
        tk.Label(inner, text=f"{icon}  {message}", font=("Helvetica", 11, "bold"),
                 bg=bg, fg="white").pack(side=tk.LEFT)

        close_btn = tk.Label(inner, text=" ✕", font=("Helvetica", 11, "bold"),
                             bg=bg, fg="white", cursor="hand2")
        close_btn.pack(side=tk.LEFT, padx=(12, 0))
        close_btn.bind("<Button-1>", lambda e: toast.destroy())

        self.root.after(3000, lambda: toast.destroy() if toast.winfo_exists() else None)

    # --- Sidebar badge ---
    def _update_badge(self):
        """Update the student count badge in the sidebar."""
        count = len(self.student_data)
        text = str(count) if count < 1000 else "999+"
        if hasattr(self, '_badge_label'):
            self._badge_label.configure(text=text)
        # Also refresh dashboard if it's the active view

    # --- Reusable UI components ---
    def _make_card(self, parent, **kwargs):
        card = tk.Frame(parent, bg=self.CARD_BG, highlightbackground=self.BORDER,
                        highlightthickness=1, **kwargs)
        return card

    def _make_heading(self, parent, text, subtitle=None):
        tk.Label(parent, text=text, font=("Helvetica", 20, "bold"),
                 bg=self.BG, fg=self.TEXT_PRIMARY, anchor="w").pack(fill=tk.X)
        if subtitle:
            tk.Label(parent, text=subtitle, font=("Helvetica", 11),
                     bg=self.BG, fg=self.TEXT_SECONDARY, anchor="w").pack(fill=tk.X, pady=(2, 0))
        tk.Frame(parent, bg=self.BG, height=20).pack(fill=tk.X)

    def _make_label(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 11, "bold"),
                 bg=self.CARD_BG, fg=self.TEXT_PRIMARY).grid(sticky=tk.W, pady=(12, 2), padx=20)

    def _make_entry(self, parent, row):
        entry = tk.Entry(parent, font=("Helvetica", 11), bg=self.INPUT_BG, fg=self.TEXT_PRIMARY,
                         relief=tk.FLAT, highlightbackground=self.BORDER, highlightcolor=self.INPUT_FOCUS,
                         highlightthickness=1, insertbackground=self.TEXT_PRIMARY)
        entry.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 5), ipady=8)
        return entry

    def _make_button(self, parent, text, command, color=None, hover=None, width=18):
        color = color or self.PRIMARY
        hover = hover or self.PRIMARY_HOVER
        btn = tk.Label(parent, text=text, font=("Helvetica", 11, "bold"), bg=color,
                       fg=self.TEXT_ON_PRIMARY, cursor="hand2", padx=20, pady=10, width=width)
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        btn.bind("<Button-1>", lambda e: command())
        return btn

    # --- Pages ---
    def show_welcome(self):
        self.clear_content()
        self._make_heading(self.content_frame, "Dashboard", "Overview of your student records")

        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg=self.BG)
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        total = len(self.student_data)
        stats = [
            ("Total Students", str(total), "👥", "#3b82f6"),
            ("Records", "Active" if total > 0 else "Empty", "📊", "#10b981"),
            ("Storage", "student_data.json", "💾", "#f59e0b"),
        ]

        for i, (label, value, icon, color) in enumerate(stats):
            card = self._make_card(stats_frame)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0 if i == 0 else 8, 0))
            inner = tk.Frame(card, bg=self.CARD_BG)
            inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)
            tk.Label(inner, text=icon, font=("Arial", 24), bg=self.CARD_BG).pack(anchor="w")
            tk.Label(inner, text=value, font=("Helvetica", 22, "bold"),
                     bg=self.CARD_BG, fg=color).pack(anchor="w", pady=(5, 0))
            tk.Label(inner, text=label, font=("Helvetica", 10),
                     bg=self.CARD_BG, fg=self.TEXT_SECONDARY).pack(anchor="w")

        # Recent students preview
        card = self._make_card(self.content_frame)
        card.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(card, bg=self.CARD_BG)
        header.pack(fill=tk.X, padx=20, pady=(15, 10))
        tk.Label(header, text="Recent Students", font=("Helvetica", 14, "bold"),
                 bg=self.CARD_BG, fg=self.TEXT_PRIMARY).pack(side=tk.LEFT)

        if self.student_data:
            items = list(self.student_data.items())[-5:]
            for roll, s in reversed(items):
                row = tk.Frame(card, bg=self.CARD_BG)
                row.pack(fill=tk.X, padx=20, pady=4)
                tk.Frame(row, bg=self.PRIMARY, width=4, height=30).pack(side=tk.LEFT, padx=(0, 12))
                tk.Label(row, text=s['name'], font=("Helvetica", 11, "bold"),
                         bg=self.CARD_BG, fg=self.TEXT_PRIMARY).pack(side=tk.LEFT)
                tk.Label(row, text=f"Roll: {roll}", font=("Helvetica", 10),
                         bg=self.CARD_BG, fg=self.TEXT_SECONDARY).pack(side=tk.LEFT, padx=(15, 0))
                tk.Label(row, text=s['email'], font=("Helvetica", 10),
                         bg=self.CARD_BG, fg=self.TEXT_SECONDARY).pack(side=tk.RIGHT)
        else:
            tk.Label(card, text="No students yet. Add one to get started.",
                     font=("Helvetica", 11), bg=self.CARD_BG, fg=self.TEXT_SECONDARY).pack(pady=20)

    def show_add_student(self):
        self.clear_content()
        self._make_heading(self.content_frame, "Add New Student", "Fill in the details below")

        card = self._make_card(self.content_frame)
        card.pack(fill=tk.X)

        form = tk.Frame(card, bg=self.CARD_BG)
        form.pack(fill=tk.X, pady=10)
        form.columnconfigure(0, weight=1)

        fields = ["Roll Number", "Name", "Phone Number (10 digits)", "Email"]
        self._add_entries = []
        for i, label in enumerate(fields):
            tk.Label(form, text=label, font=("Helvetica", 11, "bold"),
                     bg=self.CARD_BG, fg=self.TEXT_PRIMARY).grid(
                row=i * 2, column=0, sticky="w", padx=20, pady=(12, 2))
            entry = self._make_entry(form, i * 2 + 1)
            self._add_entries.append(entry)

        btn_frame = tk.Frame(card, bg=self.CARD_BG)
        btn_frame.pack(pady=(10, 20))
        self._make_button(btn_frame, "  Add Student  ", self.add_student,
                          self.SUCCESS, "#059669").pack()

    def add_student(self):
        roll, name, phone, email = [e.get().strip() for e in self._add_entries]

        if not all([roll, name, phone, email]):
            self._show_toast("All fields are required", "error")
            return
        if not roll.isdigit():
            self._show_toast("Roll number must be a valid integer", "error")
            return
        if roll in self.student_data:
            self._show_toast("A student with this roll number already exists", "error")
            return
        if not self.is_valid_name(name):
            self._show_toast("Invalid name. Only letters, spaces, hyphens, and apostrophes allowed", "error")
            return
        if not (phone.isdigit() and len(phone) == 10):
            self._show_toast("Phone number must be exactly 10 digits", "error")
            return
        if not self.is_valid_email(email):
            self._show_toast("Invalid email format", "error")
            return

        dup = self._check_duplicate('phone_number', phone)
        if dup:
            self._show_toast(f"Phone number already belongs to roll number {dup}", "error")
            return
        dup = self._check_duplicate('email', email.lower())
        if dup:
            self._show_toast(f"Email already belongs to roll number {dup}", "error")
            return

        self.student_data[roll] = {
            'name': name.title(),
            'phone_number': phone,
            'email': email.lower()
        }
        self.save_data_to_file()
        self._update_badge()
        self._show_toast("Student added successfully")
        for e in self._add_entries:
            e.delete(0, tk.END)

    def show_edit_student(self):
        self.clear_content()
        self._make_heading(self.content_frame, "Edit Student", "Search by roll number to edit")

        card = self._make_card(self.content_frame)
        card.pack(fill=tk.X)

        search_row = tk.Frame(card, bg=self.CARD_BG)
        search_row.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(search_row, text="Roll Number:", font=("Helvetica", 11, "bold"),
                 bg=self.CARD_BG, fg=self.TEXT_PRIMARY).pack(side=tk.LEFT)
        self.edit_roll_entry = tk.Entry(search_row, font=("Helvetica", 11), bg=self.INPUT_BG,
                                        fg=self.TEXT_PRIMARY, relief=tk.FLAT,
                                        highlightbackground=self.BORDER, highlightcolor=self.INPUT_FOCUS,
                                        highlightthickness=1, insertbackground=self.TEXT_PRIMARY, width=20)
        self.edit_roll_entry.pack(side=tk.LEFT, padx=12, ipady=8)
        self._make_button(search_row, "Search", self.load_student_for_edit, width=10).pack(side=tk.LEFT)

        self.edit_form_frame = tk.Frame(card, bg=self.CARD_BG)
        self.edit_form_frame.pack(fill=tk.X)

    def load_student_for_edit(self):
        for w in self.edit_form_frame.winfo_children():
            w.destroy()

        roll = self.edit_roll_entry.get().strip()
        if not roll:
            self._show_toast("Please enter a roll number", "error")
            return
        if roll not in self.student_data:
            self._show_toast("No student found with that roll number", "error")
            return

        student = self.student_data[roll]
        form = tk.Frame(self.edit_form_frame, bg=self.CARD_BG)
        form.pack(fill=tk.X, pady=10)
        form.columnconfigure(0, weight=1)

        labels = ["Name", "Phone Number", "Email"]
        values = [student['name'], student['phone_number'], student['email']]
        self._edit_entries = []
        for i, (label, val) in enumerate(zip(labels, values)):
            tk.Label(form, text=label, font=("Helvetica", 11, "bold"),
                     bg=self.CARD_BG, fg=self.TEXT_PRIMARY).grid(
                row=i * 2, column=0, sticky="w", padx=20, pady=(12, 2))
            entry = self._make_entry(form, i * 2 + 1)
            entry.insert(0, val)
            self._edit_entries.append(entry)

        btn_frame = tk.Frame(self.edit_form_frame, bg=self.CARD_BG)
        btn_frame.pack(pady=(10, 20))
        self._make_button(btn_frame, "  Update Student  ",
                          lambda: self.update_student(roll), self.SUCCESS, "#059669").pack()

    def update_student(self, roll_number):
        name, phone, email = [e.get().strip() for e in self._edit_entries]

        if not all([name, phone, email]):
            self._show_toast("All fields are required", "error")
            return
        if not self.is_valid_name(name):
            self._show_toast("Invalid name", "error")
            return
        if not (phone.isdigit() and len(phone) == 10):
            self._show_toast("Phone number must be exactly 10 digits", "error")
            return
        if not self.is_valid_email(email):
            self._show_toast("Invalid email format", "error")
            return

        dup = self._check_duplicate('phone_number', phone, exclude_roll=roll_number)
        if dup:
            self._show_toast(f"Phone number already belongs to roll number {dup}", "error")
            return
        dup = self._check_duplicate('email', email.lower(), exclude_roll=roll_number)
        if dup:
            self._show_toast(f"Email already belongs to roll number {dup}", "error")
            return

        self.student_data[roll_number] = {
            'name': name.title(),
            'phone_number': phone,
            'email': email.lower()
        }
        self.save_data_to_file()
        self._show_toast("Student updated successfully")
        self.show_edit_student()

    def show_search_student(self):
        self.clear_content()
        self._make_heading(self.content_frame, "Search Students", "Find students by any field")

        card = self._make_card(self.content_frame)
        card.pack(fill=tk.X)

        controls = tk.Frame(card, bg=self.CARD_BG)
        controls.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(controls, text="Search by:", font=("Helvetica", 11, "bold"),
                 bg=self.CARD_BG, fg=self.TEXT_PRIMARY).pack(side=tk.LEFT)

        self.search_type = tk.StringVar(value="roll")
        for text, val in [("Roll No.", "roll"), ("Name", "name"), ("Phone", "phone"), ("Email", "email")]:
            rb = tk.Radiobutton(controls, text=text, variable=self.search_type, value=val,
                                font=("Helvetica", 10), bg=self.CARD_BG, fg=self.TEXT_PRIMARY,
                                selectcolor=self.CARD_BG, activebackground=self.CARD_BG,
                                activeforeground=self.TEXT_PRIMARY, highlightthickness=0)
            rb.pack(side=tk.LEFT, padx=(12, 0))

        search_row = tk.Frame(card, bg=self.CARD_BG)
        search_row.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.search_entry = tk.Entry(search_row, font=("Helvetica", 11), bg=self.INPUT_BG,
                                     fg=self.TEXT_PRIMARY, relief=tk.FLAT,
                                     highlightbackground=self.BORDER, highlightcolor=self.INPUT_FOCUS,
                                     highlightthickness=1, insertbackground=self.TEXT_PRIMARY)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 12))
        self.search_entry.bind("<Return>", lambda e: self.search_student())
        self._make_button(search_row, "Search", self.search_student, width=10).pack(side=tk.LEFT)

        self.search_result_frame = tk.Frame(self.content_frame, bg=self.BG)
        self.search_result_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

    def search_student(self):
        for w in self.search_result_frame.winfo_children():
            w.destroy()

        val = self.search_entry.get().strip()
        stype = self.search_type.get()
        if not val:
            self._show_toast("Please enter a search value", "error")
            return

        results = []
        val_lower = val.lower()
        if stype == "roll":
            for r, s in self.student_data.items():
                if val in r:
                    results.append((r, s))
        elif stype == "name":
            for r, s in self.student_data.items():
                if val_lower in s['name'].lower():
                    results.append((r, s))
        elif stype == "phone":
            for r, s in self.student_data.items():
                if val in s['phone_number']:
                    results.append((r, s))
        elif stype == "email":
            for r, s in self.student_data.items():
                if val_lower in s['email'].lower():
                    results.append((r, s))

        if results:
            self._render_table(self.search_result_frame, results)
        else:
            tk.Label(self.search_result_frame, text="No students found matching your search.",
                     font=("Helvetica", 12), bg=self.BG, fg=self.DANGER).pack(pady=20)

    def show_all_students(self):
        self.clear_content()
        self._make_heading(self.content_frame, "All Students", f"{len(self.student_data)} records found")

        if not self.student_data:
            card = self._make_card(self.content_frame)
            card.pack(fill=tk.BOTH, expand=True)
            tk.Label(card, text="No student data available yet.", font=("Helvetica", 12),
                     bg=self.CARD_BG, fg=self.TEXT_SECONDARY).pack(pady=40)
            return

        self._current_table_data = list(self.student_data.items())
        self._current_page = 0
        self._table_container = tk.Frame(self.content_frame, bg=self.BG)
        self._table_container.pack(fill=tk.BOTH, expand=True)
        self._render_paginated_table()

    def _render_paginated_table(self):
        for w in self._table_container.winfo_children():
            w.destroy()

        data = self._current_table_data
        total = len(data)
        per_page = self.ROWS_PER_PAGE
        total_pages = max(1, (total + per_page - 1) // per_page)
        page = self._current_page
        start = page * per_page
        end = min(start + per_page, total)
        page_data = data[start:end]

        table_frame = tk.Frame(self._table_container, bg=self.BG)
        table_frame.pack(fill=tk.BOTH, expand=True)
        self._render_table(table_frame, page_data)

        if total_pages > 1:
            pag_frame = tk.Frame(self._table_container, bg=self.BG)
            pag_frame.pack(fill=tk.X, pady=(10, 0))

            prev_color = self.PRIMARY if page > 0 else self.BORDER
            prev_btn = tk.Label(pag_frame, text="← Prev", font=("Helvetica", 10, "bold"),
                                bg=prev_color, fg=self.TEXT_ON_PRIMARY, padx=14, pady=6, cursor="hand2")
            prev_btn.pack(side=tk.LEFT)
            if page > 0:
                prev_btn.bind("<Button-1>", lambda e: self._go_to_page(page - 1))
                prev_btn.bind("<Enter>", lambda e: prev_btn.configure(bg=self.PRIMARY_HOVER))
                prev_btn.bind("<Leave>", lambda e: prev_btn.configure(bg=self.PRIMARY))

            info = tk.Label(pag_frame, text=f"Page {page + 1} of {total_pages}  ({start + 1}–{end} of {total})",
                            font=("Helvetica", 10), bg=self.BG, fg=self.TEXT_SECONDARY)
            info.pack(side=tk.LEFT, expand=True)

            next_color = self.PRIMARY if page < total_pages - 1 else self.BORDER
            next_btn = tk.Label(pag_frame, text="Next →", font=("Helvetica", 10, "bold"),
                                bg=next_color, fg=self.TEXT_ON_PRIMARY, padx=14, pady=6, cursor="hand2")
            next_btn.pack(side=tk.RIGHT)
            if page < total_pages - 1:
                next_btn.bind("<Button-1>", lambda e: self._go_to_page(page + 1))
                next_btn.bind("<Enter>", lambda e: next_btn.configure(bg=self.PRIMARY_HOVER))
                next_btn.bind("<Leave>", lambda e: next_btn.configure(bg=self.PRIMARY))

    def _go_to_page(self, page):
        self._current_page = page
        self._render_paginated_table()

    def _render_table(self, parent, data):
        card = self._make_card(parent)
        card.pack(fill=tk.BOTH, expand=True)

        # Scrollable canvas
        canvas = tk.Canvas(card, bg=self.CARD_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.CARD_BG)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Header
        headers = ["Roll No.", "Name", "Phone", "Email", ""]
        widths = [10, 20, 14, 28, 8]
        header_row = tk.Frame(scroll_frame, bg=self.TABLE_HEADER_BG)
        header_row.pack(fill=tk.X)
        for h, w in zip(headers, widths):
            tk.Label(header_row, text=h, font=("Helvetica", 10, "bold"), bg=self.TABLE_HEADER_BG,
                     fg=self.TEXT_SECONDARY, width=w, anchor="w", padx=15, pady=10).pack(side=tk.LEFT)

        # Rows
        for i, (roll, s) in enumerate(data):
            bg = self.TABLE_STRIPE if i % 2 == 0 else self.CARD_BG
            row = tk.Frame(scroll_frame, bg=bg)
            row.pack(fill=tk.X)
            vals = [roll, s['name'], s['phone_number'], s['email']]
            for v, w in zip(vals, widths[:-1]):
                tk.Label(row, text=v, font=("Helvetica", 10), bg=bg,
                         fg=self.TEXT_PRIMARY, width=w, anchor="w", padx=15, pady=8).pack(side=tk.LEFT)
            # Delete button
            del_btn = tk.Label(row, text="🗑 Delete", font=("Helvetica", 9, "bold"),
                               bg=bg, fg=self.DANGER, cursor="hand2", padx=10, pady=6)
            del_btn.pack(side=tk.LEFT)
            del_btn.bind("<Enter>", lambda e, b=del_btn: b.configure(fg=self.DANGER_HOVER))
            del_btn.bind("<Leave>", lambda e, b=del_btn, c=bg: b.configure(fg=self.DANGER))
            del_btn.bind("<Button-1>", lambda e, r=roll: self._delete_student(r))

    def _delete_student(self, roll_number):
        """Delete a student after confirmation via a small dialog."""
        name = self.student_data.get(roll_number, {}).get('name', 'Unknown')

        confirm = tk.Toplevel(self.root)
        confirm.title("Confirm Delete")
        confirm.geometry("360x150")
        confirm.resizable(False, False)
        confirm.configure(bg=self.CARD_BG)
        confirm.transient(self.root)
        confirm.grab_set()

        # Center on parent
        confirm.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 360) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        confirm.geometry(f"+{x}+{y}")

        tk.Label(confirm, text=f"Delete {name} (Roll: {roll_number})?",
                 font=("Helvetica", 12, "bold"), bg=self.CARD_BG, fg=self.TEXT_PRIMARY).pack(pady=(20, 5))
        tk.Label(confirm, text="This action cannot be undone.",
                 font=("Helvetica", 10), bg=self.CARD_BG, fg=self.TEXT_SECONDARY).pack()

        btn_frame = tk.Frame(confirm, bg=self.CARD_BG)
        btn_frame.pack(pady=15)

        def do_delete():
            del self.student_data[roll_number]
            self.save_data_to_file()
            self._update_badge()
            confirm.destroy()
            self._show_toast(f"Deleted {name} (Roll: {roll_number})")
            self.show_all_students()

        cancel_btn = tk.Label(btn_frame, text="Cancel", font=("Helvetica", 10, "bold"),
                              bg=self.BORDER, fg=self.TEXT_PRIMARY, padx=18, pady=8, cursor="hand2")
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        cancel_btn.bind("<Button-1>", lambda e: confirm.destroy())

        del_btn = tk.Label(btn_frame, text="Delete", font=("Helvetica", 10, "bold"),
                           bg=self.DANGER, fg="white", padx=18, pady=8, cursor="hand2")
        del_btn.pack(side=tk.LEFT)
        del_btn.bind("<Enter>", lambda e: del_btn.configure(bg=self.DANGER_HOVER))
        del_btn.bind("<Leave>", lambda e: del_btn.configure(bg=self.DANGER))
        del_btn.bind("<Button-1>", lambda e: do_delete())

    # --- Validation & Data ---
    def _check_duplicate(self, field, value, exclude_roll=None):
        """Check if a value already exists for a given field, optionally excluding a roll number."""
        for roll, s in self.student_data.items():
            if roll == exclude_roll:
                continue
            if s[field].lower() == value.lower():
                return roll
        return None

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def is_valid_name(self, name):
        pattern = r"^[A-Za-z\s'-]+$"
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
