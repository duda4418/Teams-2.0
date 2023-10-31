import json
import tkinter as tk
from tkinter import ttk
import customtkinter

from client.contacts import get_contacts
from client.discussions import get_discussions, create_new_discussion


class DiscussionList(tk.Frame):
    def __init__(self, master=None, user_id = None):
        super().__init__(master)
        self.listbox_discussions = None
        self.button_discussions = None
        master.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.user_id = user_id
        self.create_widgets()

    def create_widgets(self):
        initial_discussions = get_discussions(self.user_id)
        self.button_discussions = customtkinter.CTkButton(self, fg_color="#fac23e", text="New Chat", hover_color="#d49d1c",
                                                          text_color="#344955", command=self.contact_window, height=60, corner_radius=20,
                                                            border_width=2, border_color="#d49d1c", font=("Arial", 16))
        self.button_discussions.pack(fill=tk.X, padx=10, pady=10)

        self.listbox_discussions = ttk.Treeview(self, selectmode="browse")
        self.listbox_discussions.pack(fill=tk.BOTH, expan=True, padx=5, pady=5, ipadx=20)
        self.listbox_discussions.heading("#0", text="Chats:" )

        for discussion in initial_discussions:
            self.listbox_discussions.insert('', 'end', text=discussion["name"], value=discussion["id"])

    def contact_window(self):
        self.root_contactwindow = tk.Toplevel()
        self.root_contactwindow.title("CONTACTS")
        self.root_contactwindow.configure(height=300, width=500, bg="#4a6572")
        self.root_contactwindow.geometry("280x400")

        self.root_contactwindow.grab_set()

        self.listbox_contacts = ttk.Treeview(self.root_contactwindow, selectmode="browse")
        self.listbox_contacts.heading("#0", text="Contacts:")
        self.listbox_contacts.pack(fill=tk.BOTH, expan=True, padx=30, pady=30)

        button_select = customtkinter.CTkButton(self.root_contactwindow, fg_color="#fac23e", text="Submit",
                                                          hover_color="#d49d1c",
                                                          text_color="#344955", height=50,
                                                          corner_radius=20,
                                                          border_width=2, border_color="#d49d1c", font=("Arial", 14),
                                                        command=self.add_selected_contact)
        button_select.pack(fill=tk.X, padx=10, pady=10)
        self.root_contactwindow.bind("<Return>", self.add_contact_event)

        contacts = get_contacts()
        for contact in contacts:
            self.listbox_contacts.insert('', 'end', text=contact["name"], value=contact["id"])

    def add_selected_contact(self):
        selected_index = self.listbox_contacts.selection()[0]
        if selected_index:
            selected_item = self.listbox_contacts.selection()[0]
            selected_discussion = self.listbox_contacts.item(selected_item)

            contact_id = str(selected_discussion["values"][0])
            contact_text = selected_discussion["text"]

            discussions = create_new_discussion(self.user_id, contact_id)
            if(discussions):
                self.listbox_discussions.insert('', 'end', text=contact_text)
            self.root_contactwindow.destroy()

    def add_contact_event(self, event):
        self.add_selected_contact()

















