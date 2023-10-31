import asyncio
import json
import tkinter as tk
from tkinter import messagebox

import customtkinter
import websocket
import websockets

from chat_app.settings import DOMAIN, PORT
from client.messages import *


class ChatMessages(tk.Frame):
    def __init__(self, master=None, discussion_list=None):
        super().__init__(master)
        master.grid(row=0, column=1, sticky="nsew")

        self.master = master
        self.chat_text = None
        self.message_entry = None
        self.send_button = None
        self.discussion_list = discussion_list
        self.placeholder = 'Type a message...'
        self.discussion_list.listbox_discussions.bind("<<TreeviewSelect>>", self.on_item_select)
        self.messages = []
        self.create_widget()


    async def connect_to_websocket_server_recv(self):
        await asyncio.sleep(2)
        try:
            async with websockets.connect(f"ws://{DOMAIN}:{PORT}/ws/yrtyrturt") as websocket:
                while True:
                    self.websocket = websocket
                    response = await websocket.recv()
                    if response:
                        self.on_item_select(response)

        except websockets.ConnectionClosed:
            messagebox.showerror("API error message", "Connection closed.")
        except Exception as e:
            messagebox.showerror("API error message", f"Error: {str(e)}")


    def on_item_select(self, event):
        selected_index = self.discussion_list.listbox_discussions.selection()

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)
        discussion_id = str(selected_discussion["values"][0])

        #Get message to API
        messages = get_messages(self.discussion_list.user_id, discussion_id)
        self.display_chat_messages(messages)

    def display_chat_messages(self, messages):
        self.chat_text.delete('1.0', tk.END)
        for message in messages:
            name = message["name"]
            value = message["value"]
            message_text = f"{name}: {value}\n\n"
            self.chat_text.insert(tk.END, message_text)

    def create_widget(self):
        self.chat_text = tk.Text(self, height=10, width=10)
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_text.config(cursor="arrow")

        self.message_entry = tk.Text(self, height=3, width=5, bg="white", fg="black")
        self.message_entry.pack(fill=tk.BOTH, padx=10, pady=10, side="top")

        self.send_button = customtkinter.CTkButton(self, fg_color="#fac23e", text="Send", hover_color="#d49d1c", text_color="#344955",
                                                   border_color="#d49d1c", border_width=2, command=self.send_message_entry)
        self.send_button.pack(fill=tk.NONE, padx=10, pady=10, ipady=5, side="right")

        self.message_entry.bind("<Return>", self.send_message_event)
        self.message_entry.insert( "1.0", self.placeholder)
        self.message_entry.config(fg="gray")
        self.message_entry.bind("<FocusIn>", self.on_message_focusin)
        self.message_entry.bind("<FocusOut>", self.on_message_focusout)

    def send_message_event(self, event):
        self.send_message_entry()

    def send_message_entry(self):
        selected_index = self.discussion_list.listbox_discussions.selection()[0]

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)

            discussion_id = str(selected_discussion["values"][0])
            message = self.message_entry.get("1.0", tk.END)

            message_obj = {
                "discussion_id": discussion_id,
                "user_id": self.discussion_list.user_id,
                "value": message
            }

            self.messages.append(message_obj)
            self.create_new_chat_messages(message_obj)
            asyncio.get_event_loop().run_until_complete(self.websocket.send("New event"))
            self.message_entry.delete('1.0', tk.END)

    def on_message_focusin(self, event):
            if self.message_entry.get("1.0", "end-1c") == self.placeholder:
                self.message_entry.delete("1.0", tk.END)
                self.message_entry.config(fg="black")

    def on_message_focusout(self, event):
            if not self.message_entry.get("1.0", "end-1c"):
                self.message_entry.insert("1.0", self.placeholder)
                self.message_entry.config(fg="gray")

    def create_new_chat_messages(self, message):
        create_new_message(message)






















