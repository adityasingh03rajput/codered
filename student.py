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
    timer_duration = timer_var.get()

    if not username:
        messagebox.showwarning("Input Error", "Please enter a username.")
        return

    if not timer_duration:
        messagebox.showwarning("Input Error", "Please select a timer duration.")
        return

    send_data("login", username)
    messagebox.showinfo("Login Success", f"Welcome, {username}!")
    root.destroy()
    start_attendance_timer(username, timer_duration)

# Function to start the attendance timer
def start_attendance_timer(username, timer_duration):
    timer_window = tk.Tk()
    timer_window.title("Attendance Timer")
    timer_window.geometry("300x200")

    timer_running = False
    remaining_time = int(timer_duration) * 60  # Convert minutes to seconds

    def update_timer():
        nonlocal remaining_time
        if timer_running and remaining_time > 0:
            mins, secs = divmod(remaining_time, 60)
            timer_label.config(text=f"Time Remaining: {mins:02}:{secs:02}")
            remaining_time -= 1
            timer_window.after(1000, update_timer)
        elif remaining_time <= 0:
            timer_label.config(text="Time's up!")
            send_data("stop_timer", username)
            messagebox.showinfo("Timer Ended", "Your attendance timer has ended.")

    def start_timer():
        nonlocal timer_running
        if not check_wifi_connection():
            messagebox.showwarning("Wi-Fi Error", "You are not connected to the authorized Wi-Fi.")
            return
        send_data("start_timer", username)
        timer_running = True
        messagebox.showinfo("Timer Started", "Your attendance is being marked.")
        update_timer()
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

    timer_label = tk.Label(timer_window, text="Time Remaining: 00:00", font=("Arial", 16))
    timer_label.pack(pady=20)

    start_button = tk.Button(timer_window, text="Start Timer", command=start_timer)
    start_button.pack(pady=10)

    stop_button = tk.Button(timer_window, text="Stop Timer", command=stop_timer)
    stop_button.pack(pady=10)

    timer_window.mainloop()

# Create the login window
root = tk.Tk()
root.title("Student Login")
root.geometry("300x200")

label_username = tk.Label(root, text="Username:")
label_username.pack(pady=10)

entry_username = tk.Entry(root)
entry_username.pack(pady=10)

label_timer = tk.Label(root, text="Select Timer Duration (minutes):")
label_timer.pack(pady=10)

# Dropdown for timer duration
timer_var = tk.StringVar(root)
timer_var.set("")  # Default value
timer_options = ["10", "20", "30", "60"]  # Timer durations in minutes
timer_dropdown = tk.OptionMenu(root, timer_var, *timer_options)
timer_dropdown.pack(pady=10)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

root.mainloop()
