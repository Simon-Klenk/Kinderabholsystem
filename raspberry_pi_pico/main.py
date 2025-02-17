# Copyright (c) 2025 Simon Klenk
# This software is licensed under the MIT License.
# See the LICENSE file in the project directory for the full license text.

import uasyncio
import ujson
import network
from microdot import Microdot
import machine
import urequests
import ubinascii
from display import Display
import time
import re

BACKEND_IP = "192.168.104.45"
BACKEND_URL_MESSAGES = f"http://{BACKEND_IP}/api/messages/"
BACKEND_URL_CLEAR = f"http://{BACKEND_IP}/api/clear/"

LED_ALERT_PIN = 2
BUTTON_ACCEPT_PIN = 15
BUTTON_REJECT_PIN = 14

led_alert = machine.Pin(LED_ALERT_PIN, machine.Pin.OUT)
button_accept = machine.Pin(BUTTON_ACCEPT_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_reject = machine.Pin(BUTTON_REJECT_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

app = Microdot()

message_id = 0
led_alert_light = False

oled_display = Display(show_text=False, new_text=False, text="Start...")

"""
!!!!!!!!!!!!!!!!!!
Before starting, the class must be executed the generate_wifi_credentials class
!!!!!!!!!!!!!!!!!!Í
"""

def connect_wifi():
    """
    Connects to the Wi-Fi network using a Base64-encoded password stored in 'wifi_pass.txt'.
    
    This function:
      - Reads the encoded password from the file.
      - Decodes the password.
      - Configures and connects to the Wi-Fi network.
      - Blocks until the connection is successfully established.
    
    Raises:
        Exception: If there is any issue reading the password file or connecting to Wi-Fi.
    """
    try:
        with open('wifi_credentials.txt', 'r') as f:
            lines = f.readlines()
            WIFI_SSID = lines[0].strip().split(": ")[1]  # Extract SSID
            encoded_password = lines[1].strip().split(": ")[1]  # Extract encoded password
    except Exception as e:
        print("Error reading Wi-Fi password file:", e)
        return

    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
    wlan.active(True)
    wlan.config(pm=0xa11140)
    
    try:
        password = ubinascii.a2b_base64(encoded_password).decode('utf-8')
    except Exception as e:
        print("Error decoding password:", e)
        return

    wlan.connect(WIFI_SSID, password)
    print("Connecting to Wi-Fi...")

    while not wlan.isconnected():
        time.sleep(1)
    print("Connected to Wi-Fi:", wlan.ifconfig())


def sanitize_text(text):
    """
    Replaces German umlauts, removes unallowed characters, trims whitespace, and limits the text length.
    
    The function replaces:
      - 'ä' with 'ae'
      - 'ö' with 'oe'
      - 'ü' with 'ue'
      - 'ß' with 'ss'
    
    It then removes all characters except letters, numbers, spaces, and specific punctuation,
    and finally limits the length of the text to 25 characters.
    
    Args:
        text (str): The input text to be sanitized.
    
    Returns:
        str: The sanitized text.
    """
    umlaut_map = {
        "ä": "ae", "ö": "oe", "ü": "ue",
        "ß": "ss", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"
    }
    
    for umlaut, replacement in umlaut_map.items():
        text = text.replace(umlaut, replacement)
    
    text = re.sub(r'[^a-zA-Z0-9 .,?!-]', '', text)
    text = text.strip()
    
    if len(text) > 25:
        text = text[:25]
    return text


@app.route('/', methods=['POST'])
async def handle_message(request):
    """
    Handles incoming POST requests to the root path.
    
    Expects a JSON payload with at least the following fields:
      - "message": The text message to be displayed.
      - "id": A unique identifier for the message.
    
    The function sanitizes the text and updates the display. An alert LED is also activated.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        tuple: A JSON response with a status message and HTTP status code.
    """
    global message_id, led_alert_light

    if not request.body:
        return {'error': 'Empty body'}, 400

    try:
        data = request.json
    except Exception as e:
        print("JSON decoding error:", e)
        return {'error': 'Invalid JSON body'}, 400

    if 'message' not in data or 'id' not in data:
        return {'error': 'Missing "message" or "id" field in JSON'}, 400

    sanitized = sanitize_text(data['message'])
    if sanitized:
        message_id = data['id']
        led_alert_light = True

        oled_display.text = sanitized
        oled_display.show_text = True
        oled_display.new_text = True

    else:
        print("Text is not valid")
        oled_display.show_text = False
        oled_display.new_text = True

    return {'status': 'Message received'}, 200

@app.route('/live', methods=['GET'])
async def check_status(request):
    """
    Handles GET requests to the '/live' endpoint.

    This endpoint is used to check if the Raspberry Pi Pico is running and responding. 
    It returns a JSON response with the device status.

    Returns:
        tuple: A JSON response with status information and HTTP status code 200.
    """
    return {'status': 'running', 'device': 'Raspberry Pi Pico'}, 

async def update_message_status(msg_id, status):
    """
    Sends a PATCH request to update the message status on the backend.
    
    The function constructs the URL using the given message ID and sends a JSON payload
    containing the status (e.g., "approved" or "rejected").
    
    Args:
        msg_id (int): The unique identifier of the message.
        status (str): The new status for the message.
    
    Raises:
        Exception: If there is an error sending the request.
    """
    url = f"{BACKEND_URL_MESSAGES}{msg_id}/"
    try:
        response = urequests.patch(url, json={"status": status})
        if response.status_code == 200:
            print(f"Status successfully sent to backend: {status}")
        else:
            print(f"Error sending status to backend: {response.status_code}")
    except Exception as e:
        print("Error sending status:", e)
    finally:
        try:
            response.close()
        except Exception:
            pass


async def monitor_buttons():
    """
    Monitors the state of the accept and reject buttons.
    
    When a button is pressed:
      - The "accept" button sends an "approved" status.
      - The "reject" button sends a "rejected" status.
    
    After sending the status, the function resets the message display and the LED alert.
    """
    global message_id, led_alert_light

    await uasyncio.sleep(2)

    while True:
        if button_accept.value() == 1 and oled_display.show_text:
            await update_message_status(message_id, "approved")
            led_alert_light = False
            message_id = 0
            oled_display.show_text = False
            oled_display.new_text = True
            await uasyncio.sleep(2)
        elif button_reject.value() == 1 and oled_display.show_text:
            await update_message_status(message_id, "rejected")
            led_alert_light = False
            message_id = 0
            oled_display.show_text = False
            oled_display.new_text = True
            await uasyncio.sleep(2)
        elif button_reject.value() == 1 and not oled_display.show_text:
            try:
                response = urequests.post(BACKEND_URL_CLEAR, json={"clear": True})
                if response.status_code == 200:
                    print(f"Clear successfully sent to backend")
                else:
                    print(f"Error sending clear to backend: {response.status_code}")
            except Exception as e:
                print("Error sending clear:", e)
            led_alert_light = False
            message_id = 0
            await uasyncio.sleep(2)
        await uasyncio.sleep(0.3)


async def control_LED():
    """
    Controls the LED by blinking it when an alert is active.
    
    The LED will blink with a 0.5-second interval if led_alert_light is True.
    Otherwise, it remains off.
    """
    global led_alert_light

    while True:
        if led_alert_light:
            led_alert.value(1)
            await uasyncio.sleep(1.5)
            led_alert.value(0)
            await uasyncio.sleep(1.5)
        else:
            led_alert.value(0)
            await uasyncio.sleep(1.5)


async def start_http_server():
    """
    Starts the HTTP server on port 80.
    
    Note:
        The app.run method is blocking, so this function must run in its own asynchronous task.
    """
    print("Starting HTTP server on port 80...")
    app.run(port=80)
    print("HTTP server running on port 80")


async def startup_display():
    """
    Displays a startup message on the OLED display for 7 seconds.
    
    The display is updated with the message "Start...", then turned off after the delay.
    """
    oled_display.text = "System laeuft"
    oled_display.show_text = True
    oled_display.new_text = True
    await uasyncio.sleep(7)
    oled_display.show_text = False
    oled_display.new_text = True


def main():
    """
    Main entry point of the application.
    
    This function:
      - Connects to the Wi-Fi network.
      - Creates asynchronous tasks for monitoring buttons, controlling the LED,
        running the HTTP server, updating the OLED display, and showing the startup message.
      - Runs the event loop indefinitely.
    """
    connect_wifi()

    loop = uasyncio.get_event_loop()
    loop.create_task(monitor_buttons())
    loop.create_task(control_LED())
    loop.create_task(start_http_server())
    loop.create_task(oled_display.print_oled())  # Assumes print_oled() is an async method in Display
    loop.create_task(startup_display())
    loop.run_forever()


if __name__ == "__main__":
    main()
