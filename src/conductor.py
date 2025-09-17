# conductor.py
# To be run on a student's computer (not the Pico)
# Requires the 'requests' library: pip install requests
import requests
import time
import json



    # --- Configuration ---
    # Students should populate this list with the IP address(es of their Picos
PICO_IPS = [
    "192.168.1.101",
    ]

def run_conductor(freq_file: str):
    with open('random_frequencies.json', "r") as f:
        data = json.load(f)

    # putting all the frequency in json file in a song list and play every note for 100 ms
    SONG = [(entry["frequency"], 100) for entry in data]

    # --- Conductor Logic ---
    def play_note_on_all_picos(freq, ms):
        """Sends a /tone POST request to every Pico in the list."""
        print(f"Playing note: {freq}Hz for {ms}ms on all devices.")

        payload = {"freq": freq, "ms": ms, "duty": 0.5}

        for ip in PICO_IPS:
            url = f"http://{ip}/tone"
            try:
                # We use a short timeout because we don't need to wait for a response
                # This makes the orchestra play more in sync.
                requests.post(url, json=payload, timeout=0.1)
            except requests.exceptions.Timeout:
                # This is expected, we can ignore it
                pass
            except requests.exceptions.RequestException as e:
                print(f"Error contacting {ip}: {e}")

    print("--- Pico Light Orchestra Conductor ---")
    print(f"Found {len(PICO_IPS)} devices in the orchestra.")
    print("Press Ctrl+C to stop.")

    try:
        # Give a moment for everyone to get ready
        print("\nStarting in 3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)
        print("Go!\n")

        # Play the song
        for note, duration in SONG:
            play_note_on_all_picos(note, duration)
            # Wait for the note's duration plus a small gap before playing the next one
            time.sleep(duration / 1000 * 1.1)

        print("\nSong finished!")

    except KeyboardInterrupt:
        print("\nConductor stopped by user.")





