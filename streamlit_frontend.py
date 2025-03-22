import streamlit as st
import time

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
    if "wifi_connected" not in st.session_state:
        st.session_state.wifi_connected = False  # Assume not connected to Wi-Fi initially

    # JavaScript to measure network speed and infer Wi-Fi connectivity
    st.components.v1.html(
        """
        <script>
        function measureNetworkSpeed() {
            const startTime = performance.now();
            fetch('https://www.google.com')
                .then(() => {
                    const endTime = performance.now();
                    const speed = (endTime - startTime) / 1000; // Speed in seconds
                    if (speed < 0.5) { // Assume Wi-Fi if speed is fast
                        window.parent.postMessage({type: 'wifiStatus', status: true}, '*');
                    } else {
                        window.parent.postMessage({type: 'wifiStatus', status: false}, '*');
                    }
                })
                .catch(() => {
                    window.parent.postMessage({type: 'wifiStatus', status: false}, '*');
                });
        }
        // Check network speed every 5 seconds
        setInterval(measureNetworkSpeed, 5000);
        </script>
        """,
        height=0,
    )

    # Listen for messages from JavaScript
    st.components.v1.html(
        """
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'wifiStatus') {
                window.parent.streamlitAPI.setComponentValue(event.data.status);
            }
        });
        </script>
        """,
        height=0,
    )

    # Start timer button
    if not st.session_state.timer_started and not st.session_state.attendance_marked:
        if st.button("Start Timer"):
            st.session_state.timer_started = True

    # Timer logic
    if st.session_state.timer_started:
        st.write("Timer is running...")
        while st.session_state.time_remaining > 0:
            # Check Wi-Fi status from session state
            if not st.session_state.wifi_connected:
                st.warning("You are not connected to Wi-Fi! Timer paused.")
                while not st.session_state.wifi_connected:
                    time.sleep(1)  # Wait for 1 second and check again
                st.success("You are now connected to Wi-Fi! Resuming timer.")

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
