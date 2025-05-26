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
from collections import deque
import time
import numpy as np

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

# Batch processing settings
BATCH_SIZE = 5  # Number of updates to process in one batch
BATCH_TIMEOUT = 0.05  # Maximum time to wait for batch in seconds

def display_image(image):
    """Display the image on the NeoPixel grid with correct snaking order"""
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert image to numpy array for faster processing
    img_array = np.array(image)
    
    # Pre-allocate the pixels array
    pixels_data = np.zeros((256, 3), dtype=np.uint8)
    
    # Process all pixels at once using numpy operations
    for y in range(16):
        row = img_array[y]
        if y % 2 == 0:
            pixels_data[y*16:(y+1)*16] = row
        else:
            pixels_data[y*16:(y+1)*16] = row[::-1]
    
    # Apply brightness
    pixels_data = (pixels_data * BRIGHTNESS).astype(np.uint8)
    
    # Update pixels
    pixels[0:256] = pixels_data.tolist()
    pixels.show()

class UpdateBatcher:
    def __init__(self, batch_size=BATCH_SIZE, batch_timeout=BATCH_TIMEOUT):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.updates = deque()
        self.last_update_time = time.time()
        self.processing = False
    
    def add_update(self, base64_image):
        self.updates.append(base64_image)
        self.last_update_time = time.time()
    
    def should_process(self):
        return (len(self.updates) >= self.batch_size or 
                (len(self.updates) > 0 and 
                 time.time() - self.last_update_time >= self.batch_timeout))
    
    def get_batch(self):
        batch = []
        while len(batch) < self.batch_size and self.updates:
            batch.append(self.updates.popleft())
        return batch

async def process_updates(batcher, websocket):
    """Process batched updates"""
    while True:
        if batcher.should_process():
            batch = batcher.get_batch()
            if not batch:
                continue
                
            # Process the last image in the batch (most recent)
            try:
                image_data = base64.b64decode(batch[-1])
                image = Image.open(io.BytesIO(image_data))
                
                if image.size != (16, 16):
                    logger.warning(f"Invalid image size: {image.size}. Expected 16x16")
                    continue
                
                display_image(image)
                
                # Send single acknowledgment for the batch
                await websocket.send(json.dumps({
                    "type": "ack",
                    "data": "batch_processed",
                    "count": len(batch)
                }))
                
            except Exception as e:
                logger.error(f"Error processing batch: {e}")
        
        await asyncio.sleep(0.01)  # Small delay to prevent CPU overload

async def connect_to_server():
    # uri = "wss://pixel-forge-sarv.replit.app/ws"
    uri = "ws://10.0.0.156:8000/ws"
    logger.info(f"Attempting to connect to {uri}")
    
    while True:
        try:
            async with websockets.connect(uri, ping_interval=20, ping_timeout=10, close_timeout=5) as websocket:
                logger.info("Connected to WebSocket server")
                
                # Send frame ID on connection
                await websocket.send(json.dumps({
                    "type": "connect",
                    "data": FRAME_ID
                }))
                
                # Initialize update batcher
                batcher = UpdateBatcher()
                
                # Start update processor
                processor_task = asyncio.create_task(process_updates(batcher, websocket))
                
                try:
                    while True:
                        message = await websocket.recv()
                        
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
                            
                            # Add update to batch
                            batcher.add_update(base64_image)
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse JSON message: {e}")
                            continue
                            
                except websockets.exceptions.ConnectionClosed:
                    logger.warning("Connection closed. Will retry in 15 seconds...")
                    processor_task.cancel()
                    await asyncio.sleep(15)  # Wait 15 seconds before retrying
                    continue
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    processor_task.cancel()
                    await asyncio.sleep(15)  # Wait 15 seconds before retrying
                    continue
                    
        except Exception as e:
            logger.error(f"Connection error: {e}")
            logger.info("Will retry in 15 seconds...")
            await asyncio.sleep(15)  # Wait 15 seconds before retrying

if __name__ == "__main__":
    logger.info("Starting frame client...")
    try:
        asyncio.run(connect_to_server())
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        # Restart the main loop
        asyncio.run(connect_to_server()) 