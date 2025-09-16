# conductor.py
# To be run on a student's computer (not the Pico)
# Requires the 'requests' library: pip install requests

import requests
import time

# --- Configuration ---
# Students should populate this list with the IP address(es of their Picos
PICO_IPS = [
    "192.168.1.101",
]

# --- Music Definition ---
# Notes mapped to frequencies (in Hz)
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523

# A simple melody: "Mary Mary had a little lamp"
# Format: (note_frequency, duration_in_ms)
SONG = [
    (E4, 400),
    (D4, 400),
    (C4, 400),
    (D4, 400),
    (E4, 400),
    (E4, 400),
    (E4, 800),

    (D4, 400),
    (D4, 400),
    (D4, 800),

    (E4, 400),
    (G4, 400),
    (G4, 800),

    (E4, 400),
    (D4, 400),
    (C4, 400),
    (D4, 400),
    (E4, 400),
    (E4, 400),
    (E4, 400),
    (E4, 400),

    (D4, 400),
    (D4, 400),
    (E4, 400),
    (D4, 400),
    (C4, 1200),
]

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


if __name__ == "__main__":
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
