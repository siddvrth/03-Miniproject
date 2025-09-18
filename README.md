# 2025 Fall ECE Senior Design Miniproject

[Project definition](./Project.md)

This project uses the Raspberry Pi Pico 2WH SC1634 (wireless, with header pins).

Each team must provide a micro-USB cable that connects to their laptop to plug into the Pi Pico.
The cord must have the data pins connected.
Splitter cords with multiple types of connectors fanning out may not have data pins connected.
Such micro-USB cords can be found locally at Microcenter, convenience stores, etc.
The student laptop is used to program the Pi Pico.
The laptop software to program and debug the Pi Pico works on macOS, Windows, and Linux.

This miniproject focuses on using
[MicroPython](./doc/micropython.md)
using
[Thonny IDE](./doc/thonny.md).
Other IDE can be used, including Visual Studio Code or
[rshell](./doc/rshell.md).

## Software Architecture
![Alt text](sw-diagram.png?raw=true)

## Issues
<img width="1280" height="442" alt="Screenshot 2025-09-18 at 9 09 45 PM" src="https://github.com/user-attachments/assets/ab03dc8e-f320-4f60-8c6e-ce0318158d90" />
<img width="1307" height="288" alt="Screenshot 2025-09-18 at 9 10 08 PM" src="https://github.com/user-attachments/assets/19c22b85-7332-4a60-8947-94d79e017a58" />
<img width="1270" height="334" alt="Screenshot 2025-09-18 at 9 10 17 PM" src="https://github.com/user-attachments/assets/af61629a-aee3-4fb5-b614-3a80a394a1ff" />
<img width="1276" height="391" alt="Screenshot 2025-09-18 at 9 10 27 PM" src="https://github.com/user-attachments/assets/5910fc4f-b634-4c0a-bdaa-7958d4eb6dbe" />
<img width="1265" height="344" alt="Screenshot 2025-09-18 at 9 15 33 PM" src="https://github.com/user-attachments/assets/86838a2e-5cee-4dd0-ac71-ba2faadee71b" />
<img width="1290" height="417" alt="Screenshot 2025-09-18 at 9 15 41 PM" src="https://github.com/user-attachments/assets/e18e0429-f9fb-45b0-a0c8-814b522240e8" />
<img width="1253" height="340" alt="Screenshot 2025-09-18 at 9 15 50 PM" src="https://github.com/user-attachments/assets/e93ccec3-9942-42ce-bad6-4119fbe45ea3" />

## Commit History
<img width="1299" height="780" alt="Screenshot 2025-09-18 at 9 12 35 PM" src="https://github.com/user-attachments/assets/a4e63f5d-dfc4-4f65-90a7-eee1b033a167" />
<img width="1285" height="625" alt="Screenshot 2025-09-18 at 9 12 44 PM" src="https://github.com/user-attachments/assets/3514fbe7-a7fe-4e3a-9779-9733b74d7edc" />

## Hardware

* Raspberry Pi Pico WH [SC1634](https://pip.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w) (WiFi, Bluetooth, with header pins)
* Freenove Pico breakout board [FNK0081](https://store.freenove.com/products/fnk0081)
* Piezo Buzzer SameSky CPT-3095C-300
* 10k ohm resistor
* 2 [tactile switches](hhttps://www.mouser.com/ProductDetail/E-Switch/TL59NF160Q?qs=QtyuwXswaQgJqDRR55vEFA%3D%3D)

### Photoresistor details

The photoresistor uses the 10k ohm resistor as a voltage divider
[circuit](./doc/photoresistor.md).
The 10k ohm resistor connects to "3V3" and to ADC2.
The photoresistor connects to the ADC2 and to AGND.
Polarity is not important for this resistor and photoresistor.

The MicroPython
[machine.ADC](https://docs.micropython.org/en/latest/library/machine.ADC.html)
class is used to read the analog voltage from the photoresistor.
The `machine.ADC(id)` value corresponds to the "GP" pin number.
On the Pico W, GP28 is ADC2, accessed with `machine.ADC(28)`.

### Piezo buzzer details

PWM (Pulse Width Modulation) can be used to generate analog signals from digital outputs.
The Raspberry Pi Pico has eight PWM groups each with two PWM channels.
The [Pico WH pinout diagram](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf)
shows that almost all Pico pins can be used for multiple distinct tasks as configured by MicroPython code or other software.
In this exercise, we will generate a PWM signal to drive a speaker.

GP16 is one of the pins that can be used to generate PWM signals.
Connect the speaker with the black wire (negative) to GND and the red wire (positive) to GP16.

In a more complete project, we would use additional resistors and capacitors with an amplifer to boost the sound output to a louder level with a bigger speaker.
The sound output is quiet but usable for this exercise.

Musical notes correspond to particular base frequencies and typically have rich harmonics in typical musical instruments.
An example soundboard showing note frequencies is [clickable](https://muted.io/note-frequencies/).
Over human history, the corresspondance of notes to frequencies has changed over time and location and musical cultures.
For the question below, feel free to use musical scale of your choice!

[Music Examples](https://github.com/twisst/Music-for-Raspberry-Pi-Pico/blob/main/play.py)


## Notes

Pico MicroPython time.sleep() doesn't error for negative values even though such are obviously incorrect--it is undefined for a system to sleep for negative time.
Duty cycle greater than 1 is undefined, so we clip the duty cycle to the range [0, 1].


## Reference

* [Pico 2WH pinout diagram](https://datasheets.raspberrypi.com/picow/pico-2-w-pinout.pdf) shows the connections to analog and digital IO.
* Getting Started with Pi Pico [book](https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf)
