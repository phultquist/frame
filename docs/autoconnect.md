# Frame Autoconnect

## What is it?
To connect to your Frame, that is to sign in with spotify, or to setup listening, or configure settings, you need to know the Frame's ip address on your network.

Of course, each device on a network has its own local ip address. You use this ip address to connect to Frame. So the goal of autoconnect is to find the Frame's local ip address.

## From Frame

To do this, we could just keep trying ips... but that's like thousands of possibilities. We also could ping around on the local network to try to find a raspberry pi, but there might be other pis on the same network, and this often isn't possible due to device security concerns.

So, to combat this, Frame sends its local ip to the server. Every 1 minute, or on start, it makes the following request which uploads the ip:

`https://patrick.today/frame/set/?ip=<LOCAL IP ADDRESS>&frameId=<FRAME ID>`

It knows its local ip address, and the Frame ID is standard in each frame.

## From your Phone

You make a request to:

`https://patrick.today/frame/connect`

On the background, here is what happens:

- The server grabs the phone's global ip
- The server finds a frame with the same global ip (that means the frame and phone are on the same network!)
  - If it can't find one, it throws an error
- Once the frame is found, the local IP is taken from a database
- The phone is redirected to the proper local ip.
