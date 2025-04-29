# loki systems app
# main.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import csv
import datetime
from database import create_database

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

def show_frame(name):
    frame = frames[name]
    frame.tkraise()

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

title_label = tk.Label(home_frame, text='Loki Systems', font=('Segoe UI', 28, 'bold'), fg=COLOR_WHITE, bg=COLOR_DARK_BLUE)
title_label.pack(pady=20)

new_service_button = ttk.Button(home_frame, text="🚀 New Service Entry")
new_service_button.pack(pady=10, ipadx=10, ipady=5)

view_services_button = ttk.Button(home_frame, text='📋 View Past Services')
view_services_button.pack(pady=10, ipadx=10, ipady=5)

monthly_report_button = ttk.Button(home_frame, text='📈 Monthly Report')
monthly_report_button.pack(pady=10, ipadx=10, ipady=5)

start_new_month_button = ttk.Button(home_frame, text="🔄 Start New Month")
start_new_month_button.pack(pady=10, ipadx=10, ipady=5)

exit_button = ttk.Button(home_frame, text='❌ Exit', command=root.quit)
exit_button.pack(pady=20, ipadx=10, ipady=5)

frames['Home'] = home_frame

# --- New Entry Frame ---
new_entry_frame = tk.Frame(root, bg=COLOR_DARK_BLUE, padx=20, pady=20)
new_entry_frame.grid(row=0, column=0, sticky='nsew')
frames['NewEntry'] = new_entry_frame

def build_new_service_frame():
    for widget in new_entry_frame.winfo_children():
        widget.destroy()

    label = tk.Label(new_entry_frame, text="🚀 New Service Entry", font=('Segoe UI', 22, 'bold'), fg=COLOR_RED, bg=COLOR_DARK_BLUE)
    label.pack(pady=10)

    fields = ["Date (YYYY-MM-DD)", "Time (HH:MM)", "Service Provided", "Service Fee", "Service Notes"]
    entries = {}

    for field in fields:
        field_label = tk.Label(new_entry_frame, text=field, font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE)
        field_label.pack(pady=(5,0))
        entry = ttk.Entry(new_entry_frame, width=40, font=global_font)
        entry.pack(pady=(0,10))
        entries[field] = entry

    def save_service():
        data = {field: entry.get() for field, entry in entries.items()}
        from database import save_service_record
        save_service_record(data)
        messagebox.showinfo("Success", "Service saved successfully!")
        show_frame('Home')

    save_button = ttk.Button(new_entry_frame, text='💾 Save Entry', command=save_service)
    save_button.pack(pady=10)

    home_button = ttk.Button(new_entry_frame, text='🏠 Home', command=lambda: show_frame('Home'))
    home_button.pack(pady=10)

# --- View Services Frame ---
view_services_frame = tk.Frame(root, bg=COLOR_DARK_BLUE, padx=20, pady=20)
view_services_frame.grid(row=0, column=0, sticky='nsew')
frames['ViewServices'] = view_services_frame

def build_view_services_frame():
    for widget in view_services_frame.winfo_children():
        widget.destroy()

    view_services_frame.rowconfigure(1, weight=1)
    view_services_frame.columnconfigure(0, weight=1)

    label = tk.Label(view_services_frame, text="📋 View Past Services", font=('Segoe UI', 22, 'bold'), fg=COLOR_RED, bg=COLOR_DARK_BLUE)
    label.grid(row=0, column=0, pady=10)
    view_services_frame.grid(row=0, column=0, sticky='nsew')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


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

    ttk.Button(button_frame, text='🗑️ Delete Selected Service', command=delete_selected).pack(pady=5)
    ttk.Button(button_frame, text='🏠 Home', command=lambda: show_frame('Home')).pack(pady=5)

# --- Monthly Report Frame ---
monthly_report_frame = tk.Frame(root, bg=COLOR_DARK_BLUE, padx=20, pady=20)
monthly_report_frame.grid(row=0, column=0, sticky='nsew')
frames['MonthlyReport'] = monthly_report_frame

def build_monthly_report_frame():
    for widget in monthly_report_frame.winfo_children():
        widget.destroy()

    label = tk.Label(monthly_report_frame, text="📈 Monthly Report", font=('Segoe UI', 22, 'bold'), fg=COLOR_RED, bg=COLOR_DARK_BLUE)
    label.pack(pady=10)

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
             font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE).pack(pady=5)
    tk.Label(monthly_report_frame, text=f"Total Services Provided: {service_count}",
             font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE).pack(pady=5)
    tk.Label(monthly_report_frame, text=f"Most Popular Service: {most_common_service}",
             font=global_font, fg=COLOR_GREEN, bg=COLOR_DARK_BLUE).pack(pady=5)

    ttk.Button(monthly_report_frame, text='🏠 Home', command=lambda: show_frame('Home')).pack(pady=20)

# --- Archive and Reset Services Function ---
def archive_and_reset_services():
    from database import fetch_all_services
    services = fetch_all_services()

    if services:
        now = datetime.datetime.now()
        filename = f"{now.strftime('%B_%Y')}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Time", "Service Provided", "Service Fee", "Service Notes"])
            for service in services:
                writer.writerow(service)

        conn = sqlite3.connect('leethal.db')
        c = conn.cursor()
        c.execute('DELETE FROM services')
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Data archived to {filename} and services reset!")
    else:
        messagebox.showinfo("No Data", "No data to archive.")

# --- Button Actions ---
new_service_button.config(command=lambda: (build_new_service_frame(), show_frame('NewEntry')))
view_services_button.config(command=lambda: (build_view_services_frame(), show_frame('ViewServices')))
monthly_report_button.config(command=lambda: (build_monthly_report_frame(), show_frame('MonthlyReport')))
start_new_month_button.config(command=archive_and_reset_services)

# --- Show Home on Startup ---
show_frame('Home')

# --- Start App ---
root.mainloop()
