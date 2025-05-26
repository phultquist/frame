import websockets
import asyncio
import base64
from PIL import Image
import io
import settings
from secrets import FRAME_ID
import os

# Ensure settings directory exists
os.makedirs("./mobile/server", exist_ok=True)

# Initialize settings if file doesn't exist
if not os.path.exists("./mobile/server/settings.json"):
    with open("./mobile/server/settings.json", "w") as f:
        f.write("{}")

# Set fixed brightness to 10%
settings.get()  # Initialize parsed
settings.put("brightness", "10")

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
                            
                        # Display the image
                        settings.get()  # Refresh settings
                        settings.put("imageUrl", "data:image/png;base64," + message)
                        
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
    asyncio.run(connect_to_server()) 