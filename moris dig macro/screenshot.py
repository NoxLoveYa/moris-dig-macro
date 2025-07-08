import sys
import os
import tempfile
from PIL import ImageGrab # For taking screenshots
import requests # For making HTTP requests

def send_screenshot_to_webhook(webhook_url, image_path):
    """Sends an image file to a Discord webhook."""
    
    # Discord webhook expects 'file' as the name for the file upload
    # and 'payload_json' for any text content or embeds.
    files = {
        'file': (os.path.basename(image_path), open(image_path, 'rb'), 'image/png')
    }
    
    try:
        response = requests.post(webhook_url, files=files)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error sending screenshot to webhook: {e}")

def take_screenshot_and_send(webhook_url):
    """Takes a full-screen screenshot, saves it, and sends it via webhook."""
    temp_dir = tempfile.gettempdir() # Get system's temporary directory
    screenshot_filename = f"screenshot_{os.getpid()}.png" # Unique filename
    screenshot_path = os.path.join(temp_dir, screenshot_filename)

    try:
        # Take a screenshot of the entire screen
        # ImageGrab.grab() captures the entire screen
        screenshot = ImageGrab.grab() 
        screenshot.save(screenshot_path, "PNG")

        # Send the screenshot to the webhook
        send_screenshot_to_webhook(webhook_url, screenshot_path)

    except Exception as e:
        print(f"An error occurred during screenshot or sending: {e}")
    finally:
        # Clean up the temporary screenshot file
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

if __name__ == "__main__":
    # Expect webhook_url as the first argument, message as the second
    if len(sys.argv) < 2:
        print("Usage: python send_screenshot.py <webhook_url>")
        sys.exit(1)

    webhook_url = sys.argv[1]

    take_screenshot_and_send(webhook_url)