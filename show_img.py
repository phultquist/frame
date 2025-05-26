import board
import neopixel
import time

# Initialize the NeoPixel strip
# Using D12 pin and 256 LEDs (16x16 grid)
pixels = neopixel.NeoPixel(board.D12, 256, auto_write=False)

def create_checkerboard():
    # Create a 16x16 checkerboard pattern
    pattern = []
    for row in range(16):
        for col in range(16):
            # Create checkerboard pattern: if row+col is even, make it white, else black
            if (row + col) % 2 == 0:
                # White color (full brightness)
                pattern.append((255, 255, 255))
            else:
                # Black color
                pattern.append((0, 0, 0))
    return pattern

def main():
    # Create the checkerboard pattern
    pattern = create_checkerboard()
    
    # Display the pattern
    pixels[0:256] = pattern[0:256]
    pixels.show()
    
    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Turn off all pixels when program is interrupted
        pixels.fill((0, 0, 0))
        pixels.show()

if __name__ == "__main__":
    main() 