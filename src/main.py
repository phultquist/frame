import websockets
import asyncio
import base64
from PIL import Image
import io
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    # Use wss:// for secure WebSocket connection
    uri = "wss://a8380e87-affe-4e91-9cf5-16d897067889-00-3u2toyoji9vca.spock.replit.dev/ws"
    logger.info(f"Attempting to connect to {uri}")
    
    while True:
        try:
            async with websockets.connect(uri, ping_interval=None) as websocket:
                logger.info("Connected to WebSocket server")
                
                # Send frame ID on connection
                await websocket.send(FRAME_ID)
                logger.info(f"Sent frame ID: {FRAME_ID}")
                
                while True:
                    try:
                        # Receive base64 encoded PNG
                        message = await websocket.recv()
                        logger.info("Received image data")
                        
                        # Decode base64 to image
                        image_data = base64.b64decode(message)
                        image = Image.open(io.BytesIO(image_data))
                        
                        # Validate image size
                        if image.size != (16, 16):
                            logger.warning(f"Invalid image size: {image.size}. Expected 16x16")
                            continue
                            
                        # Convert to RGB if needed
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                            
                        # Update display settings
                        DISPLAY_SETTINGS["imageUrl"] = "data:image/png;base64," + message
                        save_display_settings()
                        logger.info("Updated display with new image")
                        
                    except websockets.exceptions.ConnectionClosed:
                        logger.warning("Connection closed. Reconnecting...")
                        break
                    except Exception as e:
                        logger.error(f"Error processing image: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            logger.info("Waiting 5 seconds before retrying...")
            await asyncio.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    # Initialize display settings
    save_display_settings()
    logger.info("Starting frame client...")
    asyncio.run(connect_to_server()) 