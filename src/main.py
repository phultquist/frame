import websockets
import asyncio
import base64
from PIL import Image
import io
import os
import json

# Default frame ID if secrets.py doesn't exist
try:
    from secrets import FRAME_ID
except ImportError:
    FRAME_ID = "frame-1"  # Default frame ID

# Simple display settings
DISPLAY_SETTINGS = {
    "brightness": 10,
    "imageUrl": None
}

def save_display_settings():
    with open("display.json", "w") as f:
        json.dump(DISPLAY_SETTINGS, f)

async def connect_to_server():
    uri = "wss://patrick.com/frame"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                # Send frame ID on connection
                await websocket.send(FRAME_ID)
                
                while True:
                    try:
                        # Receive base64 encoded PNG
                        message = await websocket.recv()
                        
                        # Decode base64 to image
                        image_data = base64.b64decode(message)
                        image = Image.open(io.BytesIO(image_data))
                        
                        # Validate image size
                        if image.size != (16, 16):
                            print(f"Invalid image size: {image.size}. Expected 16x16")
                            continue
                            
                        # Convert to RGB if needed
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                            
                        # Update display settings
                        DISPLAY_SETTINGS["imageUrl"] = "data:image/png;base64," + message
                        save_display_settings()
                        
                    except websockets.exceptions.ConnectionClosed:
                        print("Connection closed. Reconnecting...")
                        break
                    except Exception as e:
                        print(f"Error processing image: {e}")
                        continue
                        
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    # Initialize display settings
    save_display_settings()
    asyncio.run(connect_to_server()) 