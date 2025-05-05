# loki systems app
# main.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import csv
import datetime
from database import create_database
import os 

# --- Global Styles ---
global_font = ("Segoe UI", 12)

# Colors
COLOR_BLACK = "#000000"
COLOR_RED = "#C8102E"
COLOR_GREEN = "#006B3F"
COLOR_WHITE = "#FFFFFF"
COLOR_DARK_BLUE = "#2C3E50"

# --- Initialize app window ---
root = tk.Tk()
root.title('Loki Systems')

window_width = 700
window_height = 600
root.minsize(window_width, window_height)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.configure(bg=COLOR_DARK_BLUE)
root.resizable(True, True)

# --- Create database if it doesn't exist ---
create_database()

# --- Frame system ---
frames = {}

# --- Styling ---
style = ttk.Style()
style.theme_use("default")

style.configure("TButton",
                font=("Segoe UI", 12),
                padding=10,
                background=COLOR_WHITE,
                foreground=COLOR_BLACK,
                borderwidth=1,
                relief="raised")

style.map("TButton",
          background=[('active', COLOR_GREEN)],
          foreground=[('active', COLOR_WHITE)])

style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

# --- Home Frame ---
home_frame = tk.Frame(root, bg=COLOR_DARK_BLUE, padx=20, pady=20)
home_frame.grid(row=0, column=0, sticky='nsew')

# -- setting column/row config for home frame --
home_frame.grid_columnconfigure(0, weight=1)
home_frame.grid_rowconfigure(0, weight=1)

# -- load and display logo --
logo_wrapper = tk.Frame(home_frame, bg=COLOR_DARK_BLUE)
logo_wrapper.grid(row=0, column=1, sticky="nsew", padx=60)

# -- Load and display the logo inside logo_wrapper --
logo_img = Image.open("logo.jpg")  # Make sure logo.jpg is in the same folder
logo_img = logo_img.resize((140, 140))  # Resize as needed
logo_photo = ImageTk.PhotoImage(logo_img)  # Create PhotoImage object

# -- Label to hold logo in place --
logo_label = tk.Label(root, image=logo_photo, bg=COLOR_DARK_BLUE)
logo_label.photo = logo_photo  # Save a reference to the image to avoid garbage collection

# Position it fixed at top-right using place() method
logo_label.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Adjust position as needed

# Always float above other widgets
logo_label.lift()

new_service_button = ttk.Button(home_frame, text="🚀 New Service Entry")
new_service_button.grid(row=1, column=0, pady=10, ipadx=10, ipady=5)

view_services_button = ttk.Button(home_frame, text='📋 View Past Services')
view_services_button.grid(row=2, column=0, pady=10, ipadx=10, ipady=5)

monthly_report_button = ttk.Button(home_frame, text='📈 Monthly Report')
monthly_report_button.grid(row=3, column=0, pady=10, ipadx=10, ipady=5)

start_new_month_button = ttk.Button(home_frame, text="🔄 Start New Month")
start_new_month_button.grid(row=4, column=0, pady=10, ipadx=10, ipady=5)

exit_button = ttk.Button(home_frame, text='❌ Exit', command=root.quit)
exit_button.grid(row=5, column=0, pady=10, ipadx=10, ipady=5)

frames['Home'] = home_frame

# --- New Entry Frame ---
new_entry_frame = tk.Frame(root, bg=COLOR_DARK_BLUE, padx=20, pady=20)
new_entry_frame.grid(row=0, column=0, sticky='nsew')
frames['NewEntry'] = new_entry_frame

# -- functions to show/hide logo and go home --
def show_logo():
    # Re-apply the place to make sure it's positioned right
    logo_label.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # Only .place(), no .grid
    logo_label.lift()  # Ensure it's always above all other widgets

def hide_logo():
    logo_label.place_forget()  # Cleanly removes it

def show_frame(name):
    for frame in frames.values():
        frame.grid_remove()  # Hide all frames
    frames[name].grid()     # Show the one you want

    if name == "Home":
        show_logo()
    else:
        hide_logo()

def go_home():
    show_frame('Home')

def build_new_service_frame():
    for widget in new_entry_frame.winfo_children():
        widget.destroy()

    # automatically get today's date 
    today_date = datetime.datetime.now().strftime("%y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M")  # Format: HH:MM

    label = tk.Label(new_entry_frame, text="🚀 New Service Entry", font=('Segoe UI', 22, 'bold'), fg=COLOR_RED, bg=COLOR_DARK_BLUE)
    label.grid(row=0, column=0, columnspan=2, pady=20)

    fields = ["Date (YYYY-MM-DD)", "Time (HH:MM)", "Service Provided", "Service Fee", "Service Notes"]
    entries = {}

    # Date entry field is pre-populated with today's date
    for idx, field in enumerate(fields):
        field_label = tk.Label(new_entry_frame, text=field, font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE)
        field_label.grid(row=idx + 1, column=0, sticky="e", padx=10, pady=5)

        if field == "Date (YYYY-MM-DD)":
            # Pre-fill the date field with today's date
            entry = ttk.Entry(new_entry_frame, width=40, font=global_font)
            entry.insert(0, today_date)  # Insert today's date into the entry box
        elif field == "Time (HH:MM)":
            # Pre-fill the time field with the current time
            entry = ttk.Entry(new_entry_frame, width=40, font=global_font)
            entry.insert(0, current_time)  # Insert current time into the entry box
        else:
            entry = ttk.Entry(new_entry_frame, width=40, font=global_font)
        
        entry.grid(row=idx + 1, column=1, pady=5, padx=10, sticky="w")
        entries[field] = entry

    def save_service():
        data = {field: entry.get() for field, entry in entries.items()}
        
        # call save_service_record function
        from database import save_service_record
        save_service_record(data)
        messagebox.showinfo("Success", "Service saved successfully!")
        show_frame('Home')
    
    # -- save buttons --
    save_button = ttk.Button(new_entry_frame, text='💾 Save Entry', command=save_service)
    save_button.grid(row=len(fields)+1, column=0, pady=20, padx=10)

    home_button = ttk.Button(new_entry_frame, text='🏠 Home', command=lambda:go_home())
    home_button.grid(row=len(fields)+1, column=1, pady=20, padx=10, sticky='w')

# --- View Services Frame ---
view_services_frame = tk.Frame(root, bg=COLOR_DARK_BLUE, padx=20, pady=20)
view_services_frame.grid(row=0, column=0, sticky='nsew')
frames['ViewServices'] = view_services_frame

def build_view_services_frame():
    for widget in view_services_frame.winfo_children():
        widget.destroy()
    
    # -- resizeable window & table --
    view_services_frame.rowconfigure(1, weight=1)
    view_services_frame.columnconfigure(0, weight=1)

    label = tk.Label(view_services_frame, text="📋 View Past Services", font=('Segoe UI', 22, 'bold'), fg=COLOR_RED, bg=COLOR_DARK_BLUE)
    label.grid(row=0, column=0, pady=10)
    view_services_frame.grid(row=0, column=0, sticky='nsew')
    
    # --- ** fixes bug causing logo to reposition. ( to much padding on Y axis) ** ---
    view_services_frame.grid_rowconfigure(1, weight=1)
    view_services_frame.grid_columnconfigure(0, weight=1)

    columns = ("ID", "Date", "Time", "Service", "Fee", "Notes")

    table_frame = tk.Frame(view_services_frame, bg=COLOR_DARK_BLUE)
    table_frame.grid(row=1, column=0, sticky='nsew')

    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

    y_scroll = tk.Scrollbar(table_frame, orient='vertical')
    x_scroll = tk.Scrollbar(table_frame, orient='horizontal')

    tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                        yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    y_scroll.config(command=tree.yview)
    x_scroll.config(command=tree.xview)

    tree.grid(row=0, column=0, sticky='nsew')
    y_scroll.grid(row=0, column=1, sticky='ns')
    x_scroll.grid(row=1, column=0, sticky='ew')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=120)

    from database import fetch_all_services
    services = fetch_all_services()
    for service in services:
        tree.insert("", tk.END, values=service)

    button_frame = tk.Frame(view_services_frame, bg=COLOR_DARK_BLUE)
    button_frame.grid(row=2, column=0, pady=10)

    def delete_selected():
        selected_item = tree.selection()
        if selected_item:
            item_id = selected_item[0]
            service = tree.item(item_id)['values']
            service_id = service[0]
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this service?")
            if confirm:
                from database import delete_service
                delete_service(service_id)
                tree.delete(item_id)
                messagebox.showinfo("Deleted", f"Service ID {service_id} deleted!")

    ttk.Button(button_frame, text='🗑️ Delete Selected Service', command=delete_selected).grid(pady=5)
    ttk.Button(button_frame, text='🏠 Home', command=lambda: go_home()).grid(pady=5)

# --- Monthly Report Frame ---
monthly_report_frame = tk.Frame(root, bg=COLOR_DARK_BLUE, padx=20, pady=20)
monthly_report_frame.grid(row=0, column=0, sticky='nsew')
frames['MonthlyReport'] = monthly_report_frame

def build_monthly_report_frame():
    for widget in monthly_report_frame.winfo_children():
        widget.destroy()

    label = tk.Label(monthly_report_frame, text="📈 Monthly Report", font=('Segoe UI', 22, 'bold'), fg=COLOR_RED, bg=COLOR_DARK_BLUE)
    label.grid(row=0, column=0, pady=(10, 20))

    from database import fetch_all_services
    services = fetch_all_services()

    now = datetime.datetime.now()
    current_month = now.strftime("%Y-%m")

    total_earnings = 0
    service_count = 0
    service_types = {}

    for service in services:
        raw_date = service[1]
        try:
            clean_date = raw_date.strip()
            service_date = datetime.datetime.strptime(clean_date, "%Y-%m-%d")
            if service_date.strftime("%Y-%m") == current_month:
                try:
                    total_earnings += float(service[4])
                except:
                    pass
                service_count += 1
                service_name = service[3]
                service_types[service_name] = service_types.get(service_name, 0) + 1
        except Exception as e:
            print(f"Date parse failed: {raw_date} -> {e}")

    most_common_service = max(service_types, key=service_types.get) if service_types else "N/A"

    tk.Label(monthly_report_frame, text=f"Total Earnings: /= {total_earnings:.2f}",
         font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE).grid(row=1, column=0, pady=5, sticky="w", padx=20)

    tk.Label(monthly_report_frame, text=f"Total Services Provided: {service_count}",
         font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE).grid(row=2, column=0, pady=5, sticky="w", padx=20)

    tk.Label(monthly_report_frame, text=f"Most Popular Service: {most_common_service}",
         font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE).grid(row=3, column=0, pady=5, sticky="w", padx=20)

    ttk.Button(monthly_report_frame, text='🏠 Home', command=lambda:go_home()).grid(row=4, column=0, pady=20)

# --- Archive and Reset Services Function ---
def archive_and_reset_services():
    from database import fetch_all_services, get_db_path
    services = fetch_all_services()

    if services:
        now = datetime.datetime.now()
        month_name = now.strftime("%B")
        year = now.year
        filename = f"{month_name}_{year}.csv"

        # Save to same directory as the DB (AppData)
        save_dir = os.path.dirname(get_db_path())
        full_path = os.path.join(save_dir, filename)

        with open(full_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Time", "Service Provided", "Service Fee", "Service Notes"])
            for service in services:
                writer.writerow(service)

        # Reset the database
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('DELETE FROM services')
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Data archived to {full_path} and services reset!")
    else:
        messagebox.showinfo("No Data", "No services to archive.")

# --- Button Actions ---
new_service_button.config(command=lambda: (build_new_service_frame(), show_frame('NewEntry')))
view_services_button.config(command=lambda: (build_view_services_frame(), show_frame('ViewServices')))
monthly_report_button.config(command=lambda: (build_monthly_report_frame(), show_frame('MonthlyReport')))
start_new_month_button.config(command=archive_and_reset_services)

# --- Show Home on Startup ---
show_frame('Home')

# --- Start App ---
root.mainloop()
