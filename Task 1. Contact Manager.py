#My code for the COntact Manager


import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
# File to store contacts
CONTACTS_FILE = 'contacts.json'

# Load contacts from file
def load_contacts():
    try:
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

# Add contact to list and refresh display
def add_contact():
    name = simpledialog.askstring("New Contact", "Enter contact name:")
    phone = simpledialog.askstring("New Contact", "Enter phone number:")
    email = simpledialog.askstring("New Contact", "Enter email:")

    if name and phone and email:
        contacts.append({"name": name, "phone": phone, "email": email})
        save_contacts(contacts)
        refresh_contacts()
        messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

# Edit selected contact
def edit_contact():
    selected_item = contacts_list.selection()
    if selected_item:
        contact_index = contacts_list.index(selected_item[0])
        contact = contacts[contact_index]

        # Get updated contact info
        contact['name'] = simpledialog.askstring("Edit Contact", "Update name:", initialvalue=contact['name'])
        contact['phone'] = simpledialog.askstring("Edit Contact", "Update phone number:", initialvalue=contact['phone'])
        contact['email'] = simpledialog.askstring("Edit Contact", "Update email:", initialvalue=contact['email'])

        save_contacts(contacts)
        refresh_contacts()
        messagebox.showinfo("Contact Updated", "Contact updated successfully.")
    else:
        messagebox.showwarning("Select Contact", "No contact selected for editing.")

# Delete selected contact
def delete_contact():
    selected_item = contacts_list.selection()
    if selected_item:
        contact_index = contacts_list.index(selected_item[0])
        del contacts[contact_index]
        save_contacts(contacts)
        refresh_contacts()
        messagebox.showinfo("Contact Deleted", "Contact deleted successfully.")
    else:
        messagebox.showwarning("Select Contact", "No contact selected for deletion.")

# Search contacts by name or phone
def search_contacts():
    search_term = search_entry.get().strip().lower()
    for item in contacts_list.get_children():
        contacts_list.delete(item)

    for contact in contacts:
        if search_term in contact["name"].lower() or search_term in contact["phone"]:
            contacts_list.insert("", "end", values=(contact["name"], contact["phone"], contact["email"]))

# Refresh the contact list
def refresh_contacts():
    contacts_list.delete(*contacts_list.get_children())
    for contact in contacts:
        contacts_list.insert("", "end", values=(contact["name"], contact["phone"], contact["email"]))

# Load contacts from file
contacts = load_contacts()

# Main application window
app = ttk.Window(themename="darkly")  # Choose a modern, professional theme
app.title("Contact Manager By Christabel")
app.geometry("700x450")

# Header section
header_frame = ttk.Frame(app, padding=10)
header_frame.pack(fill="x")

header_label = ttk.Label(header_frame, text="Contact Manager", font=("Helvetica", 24, "bold"), bootstyle="inverse-primary")
header_label.pack(side="left", padx=10)

# Main section with Treeview for displaying contacts
main_frame = ttk.Frame(app, padding=10)
main_frame.pack(fill="both", expand=True)

# Search bar and search button
search_frame = ttk.Frame(main_frame)
search_frame.pack(fill="x", pady=5)

search_entry = ttk.Entry(search_frame, width=40, bootstyle="info")
search_entry.pack(side="left", padx=5)
search_button = ttk.Button(search_frame, text="Search", command=search_contacts, bootstyle="primary")
search_button.pack(side="left", padx=5)

# Treeview setup
columns = ("name", "phone", "email")
contacts_list = ttk.Treeview(main_frame, columns=columns, show="headings", bootstyle="info")
contacts_list.heading("name", text="Name")
contacts_list.heading("phone", text="Phone")
contacts_list.heading("email", text="Email")
contacts_list.pack(fill="both", expand=True, padx=10, pady=10)

# Button frame for actions
button_frame = ttk.Frame(app, padding=10)
button_frame.pack(fill="x")

add_button = ttk.Button(button_frame, text="Add Contact", command=add_contact, bootstyle="success-outline")
add_button.pack(side="left", padx=5)
edit_button = ttk.Button(button_frame, text="Edit Selected", command=edit_contact, bootstyle="warning-outline")
edit_button.pack(side="left", padx=5)
delete_button = ttk.Button(button_frame, text="Delete Selected", command=delete_contact, bootstyle="danger-outline")
delete_button.pack(side="left", padx=5)

# Load initial contacts list
refresh_contacts()

# Run the application
app.mainloop()
