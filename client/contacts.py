from client.client import Client
from chat_app.settings import USER_NAME, PASSWORD
from client.urls import CONTACTS_ENDPOINT

def get_contacts():
    contacts = Client().get(CONTACTS_ENDPOINT)
    if not contacts:
        return []
    return contacts
