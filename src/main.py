
# main.py for Raspberry Pi Pico W
# Title: Pico Light Orchestra Instrument Code

import machine
import time
import network
import json
import asyncio
from light_to_note import play_tune
from data_store import save_data

# --- Pin Configuration ---
# The photosensor is connected to an Analog-to-Digital Converter (ADC) pin.
# We will read the voltage, which changes based on light.
photo_sensor_pin = machine.ADC(26)

# The buzzer is connected to a GPIO pin that supports Pulse Width Modulation (PWM).
# PWM allows us to create a square wave at a specific frequency to make a sound.
buzzer_pin = machine.PWM(machine.Pin(18))

# --- Global State ---
# This variable will hold the task that plays a note from an API call.
# This allows us to cancel it if a /stop request comes in.
api_note_task = None

# --- Core Functions ---


def connect_to_wifi(wifi_config: str = "wifi_config.json"):
    """Connects the Pico W to the specified Wi-Fi network.

    This expects a JSON text file 'wifi_config.json' with 'ssid' and 'password' keys,
    which would look like
    {
        "ssid": "your_wifi_ssid",
        "password": "your_wifi_password"
    }
    """

    with open(wifi_config, "r") as f:
        data = json.load(f)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(data["ssid"], data["password"])

    # Wait for connection or fail
    max_wait = 10
    print("Connecting to Wi-Fi...")
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError("Network connection failed")
    else:
        status = wlan.ifconfig()
        ip_address = status[0]
        print(f"Connected! Pico IP Address: {ip_address}")
    return ip_address


def play_tone(frequency: int, duration_ms: int) -> None:
    """Plays a tone on the buzzer for a given duration."""
    if frequency > 0:
        buzzer_pin.freq(int(frequency))
        buzzer_pin.duty_u16(32768)  # 50% duty cycle
        time.sleep_ms(duration_ms)  # type: ignore[attr-defined]
        stop_tone()
    else:
        time.sleep_ms(duration_ms)  # type: ignore[attr-defined]


def stop_tone():
    """Stops any sound from playing."""
    buzzer_pin.duty_u16(0)  # 0% duty cycle means silence


async def play_api_note(frequency, duration_s):
    """Coroutine to play a note from an API call, can be cancelled."""
    try:
        print(f"API playing note: {frequency}Hz for {duration_s}s")
        buzzer_pin.freq(int(frequency))
        buzzer_pin.duty_u16(32768)  # 50% duty cycle
        await asyncio.sleep(duration_s)
        stop_tone()
        print("API note finished.")
    except asyncio.CancelledError:
        stop_tone()
        print("API note cancelled.")


def map_value(x, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


async def handle_request(reader, writer):
    """Handles incoming HTTP requests."""
    global api_note_task

    print("Client connected")
    request_line = await reader.readline()
    # Skip headers
    while await reader.readline() != b"\r\n":
        pass

    try:
        request = str(request_line, "utf-8")
        method, url, _ = request.split()
        print(f"Request: {method} {url}")
    except (ValueError, IndexError):
        writer.write(b"HTTP/1.0 400 Bad Request\r\n\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    # Read current sensor value
    light_value = photo_sensor_pin.read_u16()

    response = ""
    content_type = "text/html"

    # --- API Endpoint Routing ---
    if method == "GET" and url == "/":
        html = f"""
        <html>
            <body>
                <h1>Pico Light Orchestra</h1>
                <p>Current light sensor reading: {light_value}</p>
            </body>
        </html>
        """
        response = html
    elif method == "POST" and url == "/play_note":
        # This requires reading the request body, which is not trivial.
        # A simple approach for a known content length:
        # Note: A robust server would parse Content-Length header.
        # For this student project, we'll assume a small, simple JSON body.
        raw_data = await reader.read(1024)
        try:
            data = json.loads(raw_data)
            freq = data.get("frequency", 0)
            duration = data.get("duration", 0)

            # If a note is already playing via API, cancel it first
            if api_note_task:
                api_note_task.cancel()

            # Start the new note as a background task
            api_note_task = asyncio.create_task(play_api_note(freq, duration))

            response = '{"status": "ok", "message": "Note playing started."}'
            content_type = "application/json"
        except (ValueError, json.JSONDecodeError):
            writer.write(b'HTTP/1.0 400 Bad Request\r\n\r\n{"error": "Invalid JSON"}\r\n')
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

    elif method == "POST" and url == "/stop":
        if api_note_task:
            api_note_task.cancel()
            api_note_task = None
        stop_tone()  # Force immediate stop
        response = '{"status": "ok", "message": "All sounds stopped."}'
        content_type = "application/json"
    else:
        writer.write(b"HTTP/1.0 404 Not Found\r\n\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    # Send response
    writer.write(
        f"HTTP/1.0 200 OK\r\nContent-type: {content_type}\r\n\r\n".encode("utf-8")
    )
    writer.write(response.encode("utf-8"))
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print("Client disconnected")


async def main():
    """Main execution loop."""
    try:
        ip = connect_to_wifi()
        print(f"Starting web server on {ip}...")
        asyncio.create_task(asyncio.start_server(handle_request, "0.0.0.0", 80))
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return

    # This loop runs the "default" behavior: playing sound based on light
    while True:
        # Only run this loop if no API note is currently scheduled to play
        if api_note_task is None or api_note_task.done():
            # Read the sensor. Values range from ~500 (dark) to ~65535 (bright)
            light_value = photo_sensor_pin.read_u16()

            # Map the light value to a frequency range (e.g., C4 to C6)
            # Adjust the input range based on your room's lighting
            min_light = 42500
            max_light = 65000
            min_freq = 261  # C4
            max_freq = 1046  # C6

            # Clamp the light value to the expected range
            clamped_light = max(min_light, min(light_value, max_light))

            if clamped_light > min_light:
                frequency = play_tune(clamped_light)
                buzzer_pin.freq(frequency)
                buzzer_pin.duty_u16(32768)  # 50% duty cycle
                save_data(clamped_light, frequency)
            else:
                stop_tone()  # If it's very dark, be quiet

            # Save the data 
            save_data(clamped_light, frequency)

        await asyncio.sleep_ms(50)  # type: ignore[attr-defined]


# Run the main event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped.")
        stop_tone()

