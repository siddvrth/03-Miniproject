
DATA_STORE: list = []

def save_data(brightness: float, frequency: float):
    """Saves light brightness -> buzzer frequency mapping to list in-memory."""
    DATA_STORE.append((brightness, frequency))
    print(f"Data saved: {DATA_STORE[-1]}")
