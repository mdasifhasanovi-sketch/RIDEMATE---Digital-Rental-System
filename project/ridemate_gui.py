import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import csv
import json
from datetime import datetime
import sys
import ridemate  # Our C extension

class RideMateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RideMate Vehicle Rental System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f4f8")
        self.root.minsize(800, 600)  # Set minimum window size
        self.root.resizable(True, True)  # Allow window resizing
        
        # Create a style for ttk widgets
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f4f8")
        self.style.configure("TLabel", background="#f0f4f8", font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 11))
        self.style.configure("TLabelframe", background="#f0f4f8")
        self.style.configure("TLabelframe.Label", font=("Helvetica", 12, "bold"), background="#f0f4f8")
        
        # Main container frame with padding
        self.main_frame = ttk.Frame(self.root, padding=30)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize the system
        try:
            ridemate.init_system()
            print("System initialized successfully")
        except Exception as e:
            print(f"Error initializing system: {e}")
        
        # Show the login screen
        self.show_login_screen()
        
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_frame()
        
        # App title with enhanced styling
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=25)
        ttk.Label(title_frame, text="RideMate", font=('Helvetica', 32, 'bold'), foreground="#2c3e50").pack()
        ttk.Label(title_frame, text="Vehicle Rental System", font=('Helvetica', 16), foreground="#34495e").pack()
        
        # Login Form with improved styling
        login_frame = ttk.LabelFrame(self.main_frame, text="Customer Login", padding=25)
        login_frame.pack(pady=25, padx=80, fill=tk.X)
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, pady=10, sticky=tk.W)
        self.username = ttk.Entry(login_frame, width=30)
        self.username.grid(row=0, column=1, pady=10, padx=10)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=10, sticky=tk.W)
        self.password = ttk.Entry(login_frame, show="*", width=30)
        self.password.grid(row=1, column=1, pady=10, padx=10)
        
        ttk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Options frame with better spacing
        options_frame = ttk.Frame(self.main_frame)
        options_frame.pack(pady=15)
        
        ttk.Button(options_frame, text="Register New Account", command=self.show_register_screen).pack(pady=5)
        ttk.Button(options_frame, text="Admin Login", command=self.show_admin_login).pack(pady=5)

    def show_register_screen(self):
        self.clear_frame()
        
        # Enhanced title styling
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=25)
        ttk.Label(title_frame, text="New User Registration", font=('Helvetica', 24, 'bold'), foreground="#2c3e50").pack()
        
        # Registration Form with improved styling
        reg_frame = ttk.LabelFrame(self.main_frame, text="Create Account", padding=25)
        reg_frame.pack(pady=20, padx=60, fill=tk.X)
        
        # Form fields
        fields = [
            ("Full Name:", "name"),
            ("Email:", "email"),
            ("Username:", "username"),
            ("Password:", "password"),
            ("Phone:", "phone"),
            ("Address:", "address")
        ]
        
        self.reg_entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(reg_frame, text=label).grid(row=i, column=0, pady=8, sticky=tk.W)
            entry = ttk.Entry(reg_frame, width=30)
            if field == 'password':
                entry.config(show="*")
            entry.grid(row=i, column=1, pady=8, padx=10)
            self.reg_entries[field] = entry
        
        # Register Button with improved styling
        ttk.Button(reg_frame, text="Register", command=self.register).grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        # Back to Login with better positioning
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="Back to Login", command=self.show_login_screen).pack()
    
    def show_admin_login(self):
        self.clear_frame()
        self.root.title("RideMate - Admin Login")  # Set window title
        
        # Enhanced title styling
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=25)
        ttk.Label(title_frame, text="Admin Login", font=('Helvetica', 24, 'bold'), foreground="#2c3e50").pack()
        
        # Admin Login Form with improved styling
        admin_frame = ttk.LabelFrame(self.main_frame, text="Admin Authentication", padding=25)
        admin_frame.pack(pady=25, padx=80, fill=tk.X)
        
        ttk.Label(admin_frame, text="Admin Username:").grid(row=0, column=0, pady=10, sticky=tk.W)
        self.admin_user = ttk.Entry(admin_frame, width=30)
        self.admin_user.grid(row=0, column=1, pady=10, padx=10)
        
        ttk.Label(admin_frame, text="Password:").grid(row=1, column=0, pady=10, sticky=tk.W)
        self.admin_pass = ttk.Entry(admin_frame, show="*", width=30)
        self.admin_pass.grid(row=1, column=1, pady=10, padx=10)
        
        ttk.Button(admin_frame, text="Login", command=self.admin_login).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Back button with better positioning
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="Back", command=self.show_login_screen).pack()
    
    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            # Call C backend to authenticate
            result = ridemate.authenticate_customer(username, password)
            if result is not None:
                self.current_user = {
                    'id': result['id'],
                    'name': result['name'],
                    'username': result['username'],
                    'email': result['email'],
                    'phone': result['phone']
                }
                self.show_customer_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            print(f"Login error: {e}")
            messagebox.showerror("Error", "Failed to authenticate. Please try again.")
    
    def register(self):
        # Get all registration data
        user_data = {field: entry.get() for field, entry in self.reg_entries.items()}
        
        # Basic validation
        if not all(user_data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            # Read existing customers
            with open('customers.csv', 'r') as f:
                lines = f.readlines()
            
            # Get next available ID
            if len(lines) <= 1:  # Only header or empty
                new_id = 1
            else:
                last_id = int(lines[-1].split(',')[0])  # Get ID from last line
                new_id = last_id + 1
            
            # Prepare new user data
            new_user = {
                'id': str(new_id),
                'name': user_data['name'],
                'username': user_data['username'],
                'password': user_data['password'],
                'email': user_data['email'],
                'phone': user_data['phone'],
                'active': '1'
            }
            
            # Add new user to CSV
            with open('customers.csv', 'a', newline='') as f:
                if len(lines) == 0:  # If file was empty, add header
                    f.write('id,name,username,password,email,phone,active\n')
                f.write(','.join([
                    new_user['id'],
                    f'"{new_user["name"]}"',  # Quote fields that might contain commas
                    new_user['username'],
                    new_user['password'],
                    new_user['email'],
                    new_user['phone'],
                    new_user['active']
                ]) + '\n')
            
            # Reload customer data in the C backend
            try:
                ridemate.init_system()
                messagebox.showinfo("Success", "Registration successful! You can now login with your new account.")
                self.show_login_screen()
            except Exception as e:
                print(f"Error reloading customer data: {e}")
                messagebox.showinfo("Success", "Registration successful! Please restart the application to login.")
                self.show_login_screen()
            
        except Exception as e:
            print(f"Registration error: {e}")
            messagebox.showerror("Error", "Failed to register. Please try again.")
    
    def show_admin_dashboard(self):
        self.clear_frame()
        self.root.title("RideMate - Admin Dashboard")  # Update window title
        
        # Header
        header = ttk.Frame(self.main_frame, padding="10")
        header.pack(fill=tk.X, pady=10)
        
        ttk.Label(header, text="Admin Dashboard", font=('Helvetica', 18, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header, text="Logout", command=self.show_login_screen).pack(side=tk.RIGHT, padx=10)
        
        # Create a container frame for the buttons with padding
        button_frame = ttk.Frame(self.main_frame, padding="20")
        button_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Configure the grid
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.rowconfigure(0, weight=1)
        button_frame.rowconfigure(1, weight=1)
        
        # Style for buttons
        button_style = ttk.Style()
        button_style.configure('Admin.TButton', font=('Helvetica', 12), padding=10)
        
        # Buttons for admin functions with icons and better styling
        ttk.Button(button_frame, text="Manage Vehicles", style='Admin.TButton',
                  command=self.manage_vehicles).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        ttk.Button(button_frame, text="Manage Customers", style='Admin.TButton',
                  command=self.manage_customers).grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        ttk.Button(button_frame, text="View All Rentals", style='Admin.TButton',
                  command=self.view_all_rentals).grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        ttk.Button(button_frame, text="Generate Reports", style='Admin.TButton',
                  command=self.generate_reports).grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        
        # Add some padding around the buttons
        for child in button_frame.winfo_children():
            child.grid_configure(padx=15, pady=15)
    
    def admin_login(self):
        username = self.admin_user.get()
        password = self.admin_pass.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            # Call C backend to authenticate admin
            is_authenticated = ridemate.authenticate_admin(username, password)
            if is_authenticated:
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid admin credentials")
        except Exception as e:
            print(f"Admin login error: {e}")
            messagebox.showerror("Error", "Failed to authenticate admin. Please try again.")
    
    def show_customer_dashboard(self):
        self.clear_frame()
        
        # Header
        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=10)
        
        ttk.Label(header, text="Customer Dashboard", font=('Helvetica', 18)).pack(side=tk.LEFT)
        ttk.Button(header, text="Logout", command=self.show_login_screen).pack(side=tk.RIGHT)
        
        # Tabs
        tab_control = ttk.Notebook(self.main_frame)
        
        # Available Vehicles Tab
        vehicles_tab = ttk.Frame(tab_control)
        tab_control.add(vehicles_tab, text='Available Vehicles')
        self.setup_vehicles_tab(vehicles_tab)
        
        # My Rentals Tab
        rentals_tab = ttk.Frame(tab_control)
        tab_control.add(rentals_tab, text='My Rentals')
        self.setup_rentals_tab(rentals_tab)
        
        # Profile Tab
        profile_tab = ttk.Frame(tab_control)
        tab_control.add(profile_tab, text='My Profile')
        self.setup_profile_tab(profile_tab)
        
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)
    
    def setup_vehicles_tab(self, parent):
        # Create a frame for the treeview and scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for vehicles
        columns = ("ID", "Make", "Model", "Year", "Type", "Rate/Day", "Rate/Hour", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(tree, c, is_numeric=(c in ["ID", "Year", "Rate/Day", "Rate/Hour"])))
            tree.column(col, width=100, minwidth=50, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Read vehicles from CSV
        try:
            if not os.path.exists('vehicles.csv') or os.path.getsize('vehicles.csv') == 0:
                ttk.Label(parent, text="No vehicles available").pack(pady=20)
                return
                
            with open('vehicles.csv', 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                headers = next(reader, None)  # Skip header
                
                for row in reader:
                    if len(row) >= 9:  # Ensure we have all required fields
                        status = "Available" if row[7] == '1' and row[8] == '1' else "Not Available"
                        tree.insert('', 'end', values=(
                            row[0],  # id
                            row[1],  # make
                            row[2],  # model
                            row[3],  # year
                            row[4],  # type
                            f"${row[5]}",  # ratePerDay
                            f"${row[6]}",  # ratePerHour
                            status
                        ))
            
            if not tree.get_children():
                ttk.Label(parent, text="No vehicles available").pack(pady=20)
                return
                
        except Exception as e:
            print(f"Error loading vehicles: {e}")
            ttk.Label(parent, text="Error loading vehicles").pack(pady=20)
            return
        
        # Rent button
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Rent Selected Vehicle", 
                  command=lambda: self.show_rent_dialog(tree)).pack(side=tk.LEFT, padx=5)
        
        # Add a refresh button
        ttk.Button(button_frame, text="Refresh", 
                  command=lambda: self.refresh_vehicles_tab(parent)).pack(side=tk.LEFT, padx=5)

    def refresh_vehicles_tab(self, parent):
        """Refresh the vehicles tab by re-creating it"""
        # Find the tab control and get the current tab index
        tab_control = None
        for child in parent.winfo_children():
            if isinstance(child, ttk.Notebook):
                tab_control = child
                break
        
        if tab_control:
            # Get the index of the current tab
            current_tab = tab_control.select()
            tab_index = tab_control.index(current_tab)
            
            # Recreate the tab
            tab_control.forget(current_tab)
            vehicles_tab = ttk.Frame(tab_control)
            tab_control.insert(tab_index, vehicles_tab, text='Available Vehicles')
            tab_control.select(tab_index)
            self.setup_vehicles_tab(vehicles_tab)
    
    def setup_rentals_tab(self, parent):
        if not self.current_user:
            ttk.Label(parent, text="Please log in to view rentals").pack(pady=20)
            return
            
        try:
            # Get rentals for the current user from C backend
            rentals = ridemate.get_customer_rentals(self.current_user['id'])
            if not rentals:
                ttk.Label(parent, text="No rental history found").pack(pady=20)
                return
        except Exception as e:
            print(f"Error getting rentals: {e}")
            ttk.Label(parent, text="Error loading rentals").pack(pady=20)
            return
        
        # Treeview for rentals
        columns = ("Rental ID", "Vehicle ID", "Start Date", "End Date", "Status")
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Add data
        for rental in rentals:
            tree.insert('', tk.END, values=(
                rental['id'],
                rental['vehicle_id'],
                rental['start_date'],
                rental['end_date'],
                rental['status']
            ))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_profile_tab(self, parent):
        if not self.current_user:
            ttk.Label(parent, text="Please log in to view profile").pack(pady=20)
            return
            
        # Use the current user's data
        profile = self.current_user
        
        # Display profile info
        for i, (key, value) in enumerate(profile.items()):
            ttk.Label(parent, text=f"{key.capitalize()}:", font=('Helvetica', 10, 'bold')).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            ttk.Label(parent, text=value).grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Edit button
        ttk.Button(parent, text="Edit Profile", command=self.show_edit_profile).grid(row=len(profile), column=0, columnspan=2, pady=20)
    
    def show_rent_dialog(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a vehicle to rent")
            return
            
        item = tree.item(selected[0])
        vehicle_id = item['values'][0]
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Rent Vehicle #{vehicle_id}")
        dialog.geometry("400x300")
        
        # Rental details
        ttk.Label(dialog, text=f"Renting: {item['values'][1]} {item['values'][2]}", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Rental period
        ttk.Label(dialog, text="Rental Period:").pack(pady=5)
        period_frame = ttk.Frame(dialog)
        period_frame.pack(pady=5)
        
        ttk.Label(period_frame, text="From:").grid(row=0, column=0, padx=5)
        from_date = ttk.Entry(period_frame, width=15)
        from_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        from_date.grid(row=0, column=1, padx=5)
        
        ttk.Label(period_frame, text="To:").grid(row=0, column=2, padx=5)
        to_date = ttk.Entry(period_frame, width=15)
        to_date.grid(row=0, column=3, padx=5)
        
        # Submit button
        ttk.Button(dialog, text="Confirm Rental", 
                  command=lambda: self.confirm_rental(vehicle_id, from_date.get(), to_date.get(), dialog)).pack(pady=20)
    
    def confirm_rental(self, vehicle_id, from_date, to_date, dialog):
        if not self.current_user:
            messagebox.showerror("Error", "Not logged in")
            return
            
        try:
            # Call C backend to create the rental
            rental_id = ridemate.create_rental(
                self.current_user['id'],
                vehicle_id,
                from_date,
                to_date
            )
            
            if rental_id:
                messagebox.showinfo(
                    "Success", 
                    f"Rental #{rental_id} created successfully!\n"
                    f"Vehicle: {vehicle_id}\n"
                    f"From: {from_date} to {to_date}"
                )
                # Save changes
                ridemate.save_all()
                # Refresh the view
                self.show_customer_dashboard()
            else:
                messagebox.showerror("Error", "Failed to create rental")
                
        except Exception as e:
            print(f"Error creating rental: {e}")
            messagebox.showerror("Error", f"Failed to create rental: {str(e)}")
        finally:
            dialog.destroy()
    
    def show_edit_profile(self):
        if not self.current_user:
            messagebox.showerror("Error", "Not logged in")
            return
            
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Profile")
        dialog.geometry("400x400")
        
        # Form fields
        ttk.Label(dialog, text="Edit Profile", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        fields_frame = ttk.Frame(dialog, padding=10)
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Current values
        entries = {}
        row = 0
        
        # Name
        ttk.Label(fields_frame, text="Name:").grid(row=row, column=0, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(fields_frame, width=30)
        name_entry.insert(0, self.current_user.get('name', ''))
        name_entry.grid(row=row, column=1, pady=5, padx=5)
        entries['name'] = name_entry
        row += 1
        
        # Email
        ttk.Label(fields_frame, text="Email:").grid(row=row, column=0, pady=5, sticky=tk.W)
        email_entry = ttk.Entry(fields_frame, width=30)
        email_entry.insert(0, self.current_user.get('email', ''))
        email_entry.grid(row=row, column=1, pady=5, padx=5)
        entries['email'] = email_entry
        row += 1
        
        # Phone
        ttk.Label(fields_frame, text="Phone:").grid(row=row, column=0, pady=5, sticky=tk.W)
        phone_entry = ttk.Entry(fields_frame, width=30)
        phone_entry.insert(0, self.current_user.get('phone', ''))
        phone_entry.grid(row=row, column=1, pady=5, padx=5)
        entries['phone'] = phone_entry
        row += 1
        
        # Password (optional)
        ttk.Label(fields_frame, text="New Password (leave blank to keep current):").grid(row=row, column=0, pady=5, sticky=tk.W)
        pass_entry = ttk.Entry(fields_frame, show="*", width=30)
        pass_entry.grid(row=row, column=1, pady=5, padx=5)
        entries['password'] = pass_entry
        row += 1
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Save", 
                  command=lambda: self.save_profile_changes(entries, dialog)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    # Style for buttons
    button_style = ttk.Style()
    button_style.configure('Admin.TButton', font=('Helvetica', 12), padding=10)

    def manage_vehicles(self):
        """Manage vehicles"""
        # Clear the content frame
        self.clear_frame()
        
        # Header with title and back button
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(header_frame, text="Manage Vehicles", font=('Helvetica', 16, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Back to Dashboard", 
                  command=self.show_admin_dashboard).pack(side=tk.RIGHT, padx=10)
        
        # Add new vehicle button
        ttk.Button(self.main_frame, text="Add New Vehicle", 
                  command=self.add_vehicle).pack(pady=10)
        
        # Create a frame for the table
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a treeview with scrollbars
        tree_scroll = ttk.Scrollbar(table_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.vehicles_tree = ttk.Treeview(table_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
        self.vehicles_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll.config(command=self.vehicles_tree.yview)
        
        # Define columns
        self.vehicles_tree['columns'] = ('id', 'make', 'model', 'year', 'type', 'rate_per_day', 'rate_per_hour', 'status')
        
        # Format columns
        self.vehicles_tree.column('#0', width=0, stretch=tk.NO)
        self.vehicles_tree.column('id', width=50, anchor=tk.CENTER)
        self.vehicles_tree.column('make', width=100, anchor=tk.W)
        self.vehicles_tree.column('model', width=100, anchor=tk.W)
        self.vehicles_tree.column('year', width=70, anchor=tk.CENTER)
        self.vehicles_tree.column('type', width=100, anchor=tk.W)
        self.vehicles_tree.column('rate_per_day', width=100, anchor=tk.E)
        self.vehicles_tree.column('rate_per_hour', width=100, anchor=tk.E)
        self.vehicles_tree.column('status', width=80, anchor=tk.CENTER)
        
        # Create headings
        self.vehicles_tree.heading('#0', text='', anchor=tk.W)
        self.vehicles_tree.heading('id', text='ID', anchor=tk.CENTER, command=lambda: self.sort_treeview(self.vehicles_tree, 'id', False))
        self.vehicles_tree.heading('make', text='Make', anchor=tk.W, command=lambda: self.sort_treeview(self.vehicles_tree, 'make', False))
        self.vehicles_tree.heading('model', text='Model', anchor=tk.W, command=lambda: self.sort_treeview(self.vehicles_tree, 'model', False))
        self.vehicles_tree.heading('year', text='Year', anchor=tk.CENTER, command=lambda: self.sort_treeview(self.vehicles_tree, 'year', True))
        self.vehicles_tree.heading('type', text='Type', anchor=tk.W, command=lambda: self.sort_treeview(self.vehicles_tree, 'type', False))
        self.vehicles_tree.heading('rate_per_day', text='Rate/Day', anchor=tk.E, command=lambda: self.sort_treeview(self.vehicles_tree, 'rate_per_day', True))
        self.vehicles_tree.heading('rate_per_hour', text='Rate/Hour', anchor=tk.E, command=lambda: self.sort_treeview(self.vehicles_tree, 'rate_per_hour', True))
        self.vehicles_tree.heading('status', text='Status', anchor=tk.CENTER, command=lambda: self.sort_treeview(self.vehicles_tree, 'status', False))
        
        # Add action buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add refresh button
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_vehicles_list).pack(side=tk.LEFT, padx=5)
                  
        # Add delete button
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_selected_vehicle).pack(side=tk.LEFT, padx=5)
        
        # Initial load of vehicles
        self.refresh_vehicles_list()
        
    def sort_treeview(self, tv, col, is_numeric=False, reverse=False):
        """Sort treeview by column"""
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        
        if is_numeric:
            # Convert to float if possible, otherwise use string comparison
            def try_float(x):
                try:
                    return float(x[0])
                except (ValueError, TypeError):
                    return x[0]
            l.sort(key=try_float, reverse=reverse)
        else:
            l.sort(reverse=reverse)
            
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
    def delete_selected_vehicle(self):
        """Delete the selected vehicle from the database"""
        selected = self.vehicles_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a vehicle to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected vehicle?"):
            try:
                # Get the selected item's values
                selected_item = self.vehicles_tree.item(selected[0])
                vehicle_id = str(selected_item['values'][0]).strip()  # Convert to string and strip whitespace
                print(f"Attempting to delete vehicle with ID: '{vehicle_id}'")  # Debug print
                
                # Check if file exists and has content
                if not os.path.exists('vehicles.csv') or os.path.getsize('vehicles.csv') == 0:
                    messagebox.showerror("Error", "No vehicles found in the database")
                    return
                
                # Read all vehicles
                with open('vehicles.csv', 'r', newline='', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    if not reader.fieldnames:
                        messagebox.showerror("Error", "Invalid vehicles database format")
                        return
                        
                    fieldnames = reader.fieldnames
                    vehicles = list(reader)
                    print(f"Found {len(vehicles)} vehicles in database")  # Debug print
                    print(f"Fieldnames: {fieldnames}")  # Debug print
                    if vehicles:
                        print(f"Sample vehicle data: {vehicles[0]}")  # Debug print
                
                # Filter out the vehicle to delete
                original_count = len(vehicles)
                vehicles = [v for v in vehicles if str(v.get('id', '')).strip() != vehicle_id]
                
                if len(vehicles) == original_count:
                    print(f"Vehicle with ID '{vehicle_id}' not found in database")  # Debug print
                    messagebox.showerror("Error", f"Vehicle with ID {vehicle_id} not found in database")
                    return
                
                # Create a backup of the original file
                import shutil
                backup_file = 'vehicles.csv.bak'
                shutil.copy2('vehicles.csv', backup_file)
                print(f"Created backup at {backup_file}")  # Debug print
                
                # Write remaining vehicles back to file
                with open('vehicles.csv', 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for vehicle in vehicles:
                        writer.writerow(vehicle)
                    print(f"Successfully wrote {len(vehicles)} vehicles back to file")  # Debug print
                
                # Refresh the display
                self.refresh_vehicles_list()
                messagebox.showinfo("Success", "Vehicle deleted successfully!")
                
            except Exception as e:
                error_msg = f"Failed to delete vehicle: {str(e)}"
                print(f"Error in delete_selected_vehicle: {error_msg}")  # Debug print
                import traceback
                traceback.print_exc()  # Print full traceback for debugging
                messagebox.showerror("Error", error_msg)

    def refresh_vehicles_list(self):
        """Refresh the vehicles list in the TreeView"""
        # Clear existing items
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)
            
        try:
            # Check if file exists and has content
            if not os.path.exists('vehicles.csv') or os.path.getsize('vehicles.csv') == 0:
                return
                
            # Read vehicles from CSV
            with open('vehicles.csv', 'r', newline='') as f:
                # Read the first line to check if file is empty
                first_line = f.readline().strip()
                if not first_line:  # Empty file
                    return
                    
                # Go back to start of file
                f.seek(0)
                
                # Use csv.DictReader to read the file
                reader = csv.DictReader(f)
                
                # Check if file has headers but no data
                if not any(1 for _ in reader):
                    return
                    
                # Go back to start of file again
                f.seek(0)
                next(reader)  # Skip header
                
                # Read and insert data
                for row in csv.reader(f):
                    if not row:  # Skip empty lines
                        continue
                        
                    # Make sure row has enough columns
                    if len(row) >= 9:  # Adjust number based on your CSV structure
                        status = "Available" if row[7] == '1' and row[8] == '1' else "Not Available"
                        self.vehicles_tree.insert('', 'end', values=(
                            row[0],  # id
                            row[1],  # make
                            row[2],  # model
                            row[3],  # year
                            row[4],  # type
                            f"${row[5]}",  # ratePerDay
                            f"${row[6]}",  # ratePerHour
                            status
                        ))
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load vehicles: {str(e)}")
            print(f"Error in refresh_vehicles_list: {str(e)}")  # Debug print

    def manage_customers(self):
        """Manage customers interface"""
        self.clear_frame()
        
        # Header
        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=10)
        
        ttk.Label(header, text="Manage Customers", font=('Helvetica', 18)).pack(side=tk.LEFT)
        ttk.Button(header, text="Back", command=self.show_admin_dashboard).pack(side=tk.RIGHT)
        
        # Display customers in a treeview
        columns = ("ID", "Name", "Username", "Email", "Phone", "Status")
        tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack the tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add some sample data (replace with actual data from your backend)
        customers = [
            (1, "John Doe", "johndoe", "john@example.com", "123-456-7890", "Active"),
            (2, "Jane Smith", "janesmith", "jane@example.com", "987-654-3210", "Active")
        ]
        
        for customer in customers:
            tree.insert('', tk.END, values=customer)

    def view_all_rentals(self):
        """View all rentals interface"""
        self.clear_frame()
        
        # Header
        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=10)
        
        ttk.Label(header, text="All Rentals", font=('Helvetica', 18)).pack(side=tk.LEFT)
        ttk.Button(header, text="Back", command=self.show_admin_dashboard).pack(side=tk.RIGHT)
        
        # Display rentals in a treeview
        columns = ("Rental ID", "Customer", "Vehicle", "Start Date", "End Date", "Status", "Total Cost")
        tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack the tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add some sample data (replace with actual data from your backend)
        rentals = [
            (1, "John Doe", "Toyota Corolla", "2023-01-01", "2023-01-07", "Completed", "$350"),
            (2, "Jane Smith", "Honda Civic", "2023-01-15", "2023-01-20", "Active", "$225")
        ]
        
        for rental in rentals:
            tree.insert('', tk.END, values=rental)

    def generate_reports(self):
        """Generate reports interface"""
        self.clear_frame()
        
        # Header
        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=10)
        
        ttk.Label(header, text="Generate Reports", font=('Helvetica', 18)).pack(side=tk.LEFT)
        ttk.Button(header, text="Back", command=self.show_admin_dashboard).pack(side=tk.RIGHT)
        
        # Report options frame
        report_frame = ttk.LabelFrame(self.main_frame, text="Select Report Type", padding=20)
        report_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Report type selection
        report_type = tk.StringVar()
        reports = [
            "Monthly Revenue Report",
            "Vehicle Utilization Report",
            "Customer Activity Report",
            "Rental History Report"
        ]
        
        for i, report in enumerate(reports):
            ttk.Radiobutton(report_frame, text=report, variable=report_type, 
                           value=report).pack(anchor=tk.W, pady=5)
        
        # Date range selection
        date_frame = ttk.Frame(report_frame)
        date_frame.pack(pady=20, fill=tk.X)
        
        ttk.Label(date_frame, text="From:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(date_frame, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(date_frame, text="To:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(date_frame, width=15).pack(side=tk.LEFT, padx=5)
        
        # Generate button
        ttk.Button(report_frame, text="Generate Report", 
                  command=lambda: self.generate_report(report_type.get())).pack(pady=20)

    def add_vehicle(self, entries=None, dialog=None):
        """Add a new vehicle"""
        if dialog is None:  # If not called from save_vehicle
            dialog = tk.Toplevel(self.root)
            dialog.title("Add New Vehicle")
            dialog.geometry("400x400")
            dialog.transient(self.root)  # Set to be on top of the main window
            dialog.grab_set()  # Modal dialog
            
            # Create form fields
            fields = ["Make", "Model", "Year", "Type", "Rate per Day", "Rate per Hour"]
            entries = {}
            
            for field in fields:
                frame = ttk.Frame(dialog)
                frame.pack(fill=tk.X, padx=5, pady=5)
                label = field + ":"
                ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT)
                entry = ttk.Entry(frame)
                entry.pack(fill=tk.X, padx=5, expand=True)
                entries[field.lower().replace(" ", "_")] = entry
            
            # Add buttons
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=20)
            
            ttk.Button(button_frame, text="Save", 
                      command=lambda: self.save_vehicle(entries, dialog)).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Cancel", 
                      command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        else:
            # If called from save_vehicle, just save the data
            self.save_vehicle(entries, dialog)

    def save_vehicle(self, entries, dialog):
        """Save the new vehicle to the database"""
        try:
            # Get all the values from the form
            make = entries['make'].get()
            model = entries['model'].get()
            year = entries['year'].get()
            vehicle_type = entries['type'].get()
            rate_per_day = entries['rate_per_day'].get()
            rate_per_hour = entries['rate_per_hour'].get()
        
            # Validate inputs
            if not all([make, model, year, vehicle_type, rate_per_day, rate_per_hour]):
                messagebox.showerror("Error", "All fields are required!")
                return
                
            # Generate a new vehicle ID
            next_id = 1
            try:
                with open('vehicles.csv', 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 1:  # If there are existing vehicles
                        last_id = int(lines[-1].split(',')[0])
                        next_id = last_id + 1
            except FileNotFoundError:
                pass  # File doesn't exist yet, we'll create it
                
            # Prepare the vehicle data
            vehicle_data = [
                str(next_id),  # ID
                make,
                model,
                year,
                vehicle_type,
                rate_per_day,
                rate_per_hour,
                '1',  # active
                '1'   # available
            ]
            
            # Write to CSV
            with open('vehicles.csv', 'a', newline='') as f:
                import csv
                writer = csv.writer(f)
                # Write header if file is empty
                if f.tell() == 0:
                    writer.writerow(['id', 'make', 'model', 'year', 'type', 'ratePerDay', 'ratePerHour', 'active', 'available'])
                writer.writerow(vehicle_data)
            
            messagebox.showinfo("Success", "Vehicle added successfully!")
            dialog.destroy()
            self.manage_vehicles()  # Refresh the vehicles list
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save vehicle: {str(e)}")

def main():
    # Create the main window first
    root = tk.Tk()
    
    # Remove window decorations (including icon)
    root.overrideredirect(True)
    
    # Set the window title and other attributes
    root.title("RideMate Vehicle Rental System")
    
    # Re-enable window decorations but without the icon
    root.after(100, lambda: root.overrideredirect(False))
    
    # On Windows, prevent the default icon from showing
    if sys.platform.startswith('win'):
        try:
            root.iconbitmap('')
        except:
            pass
    
    # Initialize the application
    app = RideMateGUI(root)
    
    # Make sure the window is properly sized
    root.update_idletasks()
    
    # Start the main event loop
    root.mainloop()
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    # Ensure proper cleanup on exit
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
