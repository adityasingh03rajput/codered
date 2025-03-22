import tkinter as tk
from tkinter import messagebox
import socket
import json
import threading
import subprocess

# Server configuration
HOST = "127.0.0.1"
PORT = 65432

# Authorized Wi-Fi BSSID
AUTHORIZED_BSSID = "ee:ee:6d:9d:6f:ba"  # Replace with your school's Wi-Fi BSSID

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to check Wi-Fi connection
def check_wifi_connection():
    """Check if the device is connected to the authorized Wi-Fi using BSSID."""
    try:
        # Use 'netsh' to get Wi-Fi interface details (Windows only)
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True
        )
        # Extract BSSID from the output
        for line in result.stdout.splitlines():
            if "BSSID" in line:
                bssid = ":".join(line.split(":")[1:]).strip().lower()
                if bssid == AUTHORIZED_BSSID.lower():
                    return True
    except Exception as e:
        messagebox.showerror("Error", f"Error checking Wi-Fi status: {e}")
    return False

# Function to send data to the server
def send_data(action, username=None):
    data = {"action": action, "username": username}
    client_socket.send(json.dumps(data).encode("utf-8"))

# Function to handle login
def login():
    username = entry_username.get()
    if not username:
        messagebox.showwarning("Input Error", "Please enter a username.")
        return

    send_data("login", username)
    messagebox.showinfo("Login Success", f"Welcome, {username}!")
    root.destroy()
    start_attendance_timer(username)

# Function to start the attendance timer
def start_attendance_timer(username):
    timer_window = tk.Tk()
    timer_window.title("Attendance Timer")
    timer_window.geometry("300x200")

    timer_running = False

    def start_timer():
        nonlocal timer_running
        if not check_wifi_connection():
            messagebox.showwarning("Wi-Fi Error", "You are not connected to the authorized Wi-Fi.")
            return
        send_data("start_timer", username)
        timer_running = True
        messagebox.showinfo("Timer Started", "Your attendance is being marked.")
        monitor_wifi(username)

    def stop_timer():
        nonlocal timer_running
        send_data("stop_timer", username)
        timer_running = False
        messagebox.showinfo("Timer Stopped", "Your attendance is no longer being marked.")

    def monitor_wifi(username):
        if timer_running:
            if not check_wifi_connection():
                send_data("stop_timer", username)
                messagebox.showwarning("Wi-Fi Disconnected", "You are no longer connected to the authorized Wi-Fi.")
            else:
                timer_window.after(5000, monitor_wifi, username)  # Check every 5 seconds

    start_button = tk.Button(timer_window, text="Start Timer", command=start_timer)
    start_button.pack(pady=20)

    stop_button = tk.Button(timer_window, text="Stop Timer", command=stop_timer)
    stop_button.pack(pady=20)

    timer_window.mainloop()

# Create the login window
root = tk.Tk()
root.title("Student Login")
root.geometry("300x150")

label_username = tk.Label(root, text="Username:")
label_username.pack(pady=10)

entry_username = tk.Entry(root)
entry_username.pack(pady=10)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

root.mainloop()
