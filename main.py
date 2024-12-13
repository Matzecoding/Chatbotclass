from openai import OpenAI
from event_handler import MyEventHandler
from wiki_utills import login_to_wiki
import os
from config import assistant_id
import streamlit as st


def initialize_chatbot():
    """Initialisiert den OpenAI-Client und die Wiki-Session."""
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    session = login_to_wiki("Matze", "Head$ripyeah")  # Beispiel-Login-Daten
    vector_store_id = "vs_56heQwFcoW60pFQuPCX48O8l"
    thread = client.beta.threads.create()
    return client, session, thread, vector_store_id


def send_message(client, session, thread, vector_store_id, user_message):
    """Sendet eine Nachricht an den Chatbot und empfängt die Antwort."""
    # Nachricht an den Assistant senden
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    # Antwort vom Chatbot streamen
    handler = MyEventHandler(client, thread.id, session, assistant_id, vector_store_id)
    with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant_id,
            event_handler=handler
    ) as stream:
        stream.until_done()  # Warten, bis der Assistant fertig ist

    # Rückgabe der vollständigen Antwort
    return handler.latest_response  # `latest_response` musst du in `MyEventHandler` hinzufügen
