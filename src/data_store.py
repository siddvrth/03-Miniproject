import time
import _thread

DATA_STORE: list = []
last_print_time = 0

def save_data(brightness: float, frequency: float):
    """Saves light brightness -> buzzer frequency mapping to list in-memory."""
    DATA_STORE.append((brightness, frequency))

def print_data_continuously():
    """Prints the most recent data entry exactly once per second"""
    global last_print_time
    
    while True:
        current_time = time.time()
        if current_time - last_print_time >= 1:  # Check if 1 second has elapsed
            if DATA_STORE:  # Check if there's any data
                print(f"Current reading: {DATA_STORE[-1]}")
            last_print_time = current_time
        time.sleep(0.1)  # Small sleep to prevent busy waiting

# Start the continuous printing in a separate thread
_thread.start_new_thread(print_data_continuously, ())