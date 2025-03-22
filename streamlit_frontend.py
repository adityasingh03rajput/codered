import streamlit as st
import time

# JavaScript to check internet connectivity
check_online_js = """
<script>
function checkOnline() {
    return navigator.onLine;
}
</script>
"""

# Streamlit app
def main():
    st.title("Attendance Timer 🕒")
    st.write("Start the timer to mark your attendance. The timer will only run if you're connected to the internet.")

    # Initialize session state for timer
    if "timer_started" not in st.session_state:
        st.session_state.timer_started = False
    if "time_remaining" not in st.session_state:
        st.session_state.time_remaining = 10  # Set timer duration (10 seconds)
    if "attendance_marked" not in st.session_state:
        st.session_state.attendance_marked = False

    # Inject JavaScript to check online status
    st.components.v1.html(check_online_js)

    # Start timer button
    if not st.session_state.timer_started and not st.session_state.attendance_marked:
        if st.button("Start Timer"):
            st.session_state.timer_started = True

    # Timer logic
    if st.session_state.timer_started:
        st.write("Timer is running...")
        while st.session_state.time_remaining > 0:
            # Check online status using JavaScript
            online_status = st.components.v1.html(
                """
                <script>
                document.write(navigator.onLine);
                </script>
                """,
                height=0,
            )
            online_status = online_status.strip() == "true"

            if not online_status:
                st.warning("You are offline! Timer paused.")
                while not online_status:
                    time.sleep(1)  # Wait for 1 second and check again
                    online_status = st.components.v1.html(
                        """
                        <script>
                        document.write(navigator.onLine);
                        </script>
                        """,
                        height=0,
                    )
                    online_status = online_status.strip() == "true"
                st.success("You are back online! Resuming timer.")

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
