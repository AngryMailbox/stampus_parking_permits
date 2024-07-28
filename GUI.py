import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
from pathlib import Path
from parking import create_parking_permit
import database

class ParkingPermitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parkeringstillstånd/Parking Permit")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.logo_path = self.resource_path("logo.png")
        self.icon_path = self.resource_path("logo.ico")
        self.root.iconbitmap(self.icon_path)

        self.create_widgets()

    def create_widgets(self):
        # Inputs
        self.name_entry = self.create_entry("Namn/Name")
        self.position_entry = self.create_entry("Befattning/Position")
        self.valid_until_entry = self.create_date_entry("Gäller till/Valid Until")

        # Submit
        generate_button = ctk.CTkButton(self.root, text="Skapa tillstånd/Create Permit", command=self.generate_permit, fg_color='purple')
        generate_button.pack(pady=20)

        # View Permits
        view_button = ctk.CTkButton(self.root, text="Visa tillstånd/View permits", command=self.view_permits, fg_color='purple')
        view_button.pack(pady=10)

    def create_entry(self, placeholder):
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=5, padx=20, fill='x')
        label = ctk.CTkLabel(frame, text=placeholder)
        label.pack(side='left', padx=10)
        entry = ctk.CTkEntry(frame)
        entry.pack(side='left', fill='x', expand=True)
        return entry

    def create_date_entry(self, placeholder):
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=5, padx=20, fill='x')
        label = ctk.CTkLabel(frame, text=placeholder)
        label.pack(side='left', padx=10)
        date_entry = DateEntry(frame, date_pattern='dd/mm/yyyy')
        date_entry.pack(side='left', fill='x', expand=True)
        return date_entry

    def generate_permit(self):
        name = self.name_entry.get()
        position = self.position_entry.get()
        valid_until = self.valid_until_entry.get()

        if not (name and position and valid_until):
            messagebox.showerror("Input Error", "Vänligen fyll i alla fält/Please fill in all fields")
            return

        
        
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], title="Save Parking Permit As", initialfile=f"{name}_permit.png")
        if save_path:
            new_permit_number = database.add_permit(name, position, valid_until, save_path)
            messagebox.showinfo("Success", f"Tillstånd skapat Nr/Parking permit created No: {new_permit_number}")
            permit = create_parking_permit(name, position, new_permit_number, valid_until)
            permit.save(Path(save_path))
            permit.show()

    def view_permits(self):
        permits = database.get_permits()
        permits_window = ctk.CTkToplevel(self.root)
        permits_window.title("View and Manage Permits")
        permits_window.geometry("700x500")
        permits_window.attributes("-topmost", True)

        columns = ('_id', 'name', 'position', 'permit_number', 'valid_until', 'file_path')
        tree = ttk.Treeview(permits_window, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for permit in permits:
            tree.insert('', 'end', values=(permit['_id'], permit['name'], permit['position'], permit['permit_number'], permit['valid_until'], permit['file_path']))

        tree.pack(fill='both', expand=True)

        def delete_selected():
            if not tree.selection():
                messagebox.showerror("Error", "Vänligen välj ett tillstånd/Please select a permit")
                return
            selected_item = tree.selection()[0]
            permit_id = tree.item(selected_item)['values'][0]
            print("PERMIT:ID", permit_id)
            delete_count = database.delete_permit(permit_id)
            if delete_count:
                tree.delete(selected_item)
                messagebox.showinfo("Success", "Tillstånd borttaget/Permit deleted", parent=permits_window)
            else:
                messagebox.showerror("Error", "Failed to delete permit", parent=permits_window)

            # Refresh permits
            tree.delete(*tree.get_children())
            permits = database.get_permits()
            for permit in permits:
                tree.insert('', 'end', values=(permit['_id'], permit['name'], permit['position'], permit['permit_number'], permit['valid_until'], permit['file_path']))

        delete_button = ctk.CTkButton(permits_window, text="Delete Selected Permit", command=delete_selected)
        delete_button.pack(pady=10)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = ParkingPermitGUI(root)
    root.mainloop()
