import streamlit as st
import time
import subprocess

# Function to check Wi-Fi connection on Windows
def check_wifi_connection():
    try:
        # Use 'netsh' to check Wi-Fi connection status
        result = subprocess.run(
            ["netsh", "interface", "show", "interface", "Wi-Fi"],
            capture_output=True, text=True
        )
        # Check if the output contains "Connected"
        if "Connected" in result.stdout:
            return True
    except Exception as e:
        st.error(f"Error checking Wi-Fi status: {e}")
    return False

# Streamlit app
def main():
    st.title("Attendance Timer 🕒")
    st.write("Start the timer to mark your attendance. The timer will only run if you're connected to Wi-Fi.")

    # Initialize session state for timer
    if "timer_started" not in st.session_state:
        st.session_state.timer_started = False
    if "time_remaining" not in st.session_state:
        st.session_state.time_remaining = 10  # Set timer duration (10 seconds)
    if "attendance_marked" not in st.session_state:
        st.session_state.attendance_marked = False

    # Start timer button
    if not st.session_state.timer_started and not st.session_state.attendance_marked:
        if st.button("Start Timer"):
            st.session_state.timer_started = True

    # Timer logic
    if st.session_state.timer_started:
        st.write("Timer is running...")
        while st.session_state.time_remaining > 0:
            if not check_wifi_connection():
                st.warning("Wi-Fi disconnected! Timer paused.")
                while not check_wifi_connection():
                    time.sleep(1)  # Wait for 1 second and check again
                st.success("Wi-Fi reconnected! Resuming timer.")

            st.write(f"Time remaining: {st.session_state.time_remaining} seconds")
            time.sleep(1)  # Wait for 1 second
            st.session_state.time_remaining -= 1

        st.session_state.timer_started = False
        st.session_state.attendance_marked = True
        st.success("Time's up! Attendance Marked. 🎉")

    # Reset button
    if st.session_state.attendance_marked:
        if st.button("Reset Timer"):
            st.session_state.timer_started = False
            st.session_state.time_remaining = 10
            st.session_state.attendance_marked = False
            st.experimental_rerun()  # Refresh the app

# Run the Streamlit app
if __name__ == "__main__":
    main()
