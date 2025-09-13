THRESHOLDS = [44500, 47000, 50000, 54000]
FREQUENCIES = [262, 294, 330, 349, 392]

def play_tune(light_freq: int) -> int:
    if light_freq < THRESHOLDS[0]:
        return FREQUENCIES[0]
    elif light_freq < THRESHOLDS[1]:
        return FREQUENCIES[1]
    elif light_freq < THRESHOLDS[2]:
        return FREQUENCIES[2]
    elif light_freq < THRESHOLDS[3]:
        return FREQUENCIES[3]
    else:
        return FREQUENCIES[4]