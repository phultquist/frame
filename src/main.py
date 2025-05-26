import websockets
import asyncio
import base64
from PIL import Image
import io
import os
import json
import logging
import board
import neopixel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(board.D12, 256, auto_write=False)

# Default frame ID if secrets.py doesn't exist
try:
    from secrets import FRAME_ID
except ImportError:
    FRAME_ID = "frame-1"  # Default frame ID

# Fixed brightness at 10%
BRIGHTNESS = 0.10

def display_image(image):
    """Display the image on the NeoPixel grid with correct snaking order"""
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixels_data = [(0, 0, 0)] * 256  # Pre-fill with black
    for y in range(16):
        for x in range(16):
            r, g, b = image.getpixel((x, y))
            r = int(r * BRIGHTNESS)
            g = int(g * BRIGHTNESS)
            b = int(b * BRIGHTNESS)
            if y % 2 == 0:
                idx = y * 16 + x
            else:
                idx = y * 16 + (15 - x)
            pixels_data[idx] = (r, g, b)
    pixels[0:256] = pixels_data
    pixels.show()

async def connect_to_server():
    uri = "wss://pixel-forge-sarv.replit.app/ws"
    logger.info(f"Attempting to connect to {uri}")
    
    while True:
        try:
            async with websockets.connect(uri, ping_interval=None) as websocket:
                logger.info("Connected to WebSocket server")
                
                # Send frame ID on connection
                await websocket.send(json.dumps({
                    "type": "connect",
                    "data": FRAME_ID
                }))
                logger.info(f"Sent frame ID: {FRAME_ID}")
                
                while True:
                    try:
                        # Receive JSON message
                        message = await websocket.recv()
                        
                        # Parse JSON message
                        try:
                            data = json.loads(message)
                            message_type = data.get("type")
                            
                            if message_type == "error":
                                error_msg = data.get("message", "Unknown error")
                                logger.error(f"Server error: {error_msg}")
                                continue
                                
                            if message_type != "image_update":
                                logger.warning(f"Unexpected message type: {message_type}")
                                continue
                                
                            base64_image = data.get("data")
                            if not base64_image:
                                logger.warning("No image data in message")
                                continue
                                
                            # Decode base64 to image
                            image_data = base64.b64decode(base64_image)
                            image = Image.open(io.BytesIO(image_data))
                            
                            # Validate image size
                            if image.size != (16, 16):
                                logger.warning(f"Invalid image size: {image.size}. Expected 16x16")
                                continue
                                
                            # Display the image on the NeoPixel grid immediately
                            display_image(image)
                            
                            # Send acknowledgment
                            await websocket.send(json.dumps({
                                "type": "ack",
                                "data": "image_received"
                            }))
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse JSON message: {e}")
                            continue
                        
                    except websockets.exceptions.ConnectionClosed:
                        logger.warning("Connection closed. Reconnecting...")
                        break
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Connection error: {e}")
            logger.info("Waiting 5 seconds before retrying...")
            await asyncio.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    logger.info("Starting frame client...")
    asyncio.run(connect_to_server()) 