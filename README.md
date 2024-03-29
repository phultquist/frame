# [Frame](https://patrick.app/project/frame)
A Summer of Making Project by Addison and Patrick. 
![1d318fd0c7d2752428f7d16fac4e24e8edbbd3c5-750x1246](https://user-images.githubusercontent.com/46694203/173881306-22dbde9e-0080-431c-b2c3-8a92593f4726.jpg)


**Funded by GitHub through Hack Club.**

### A Note About the Code
As of right now, the code contains both NodeJS files and Python files. Since I'm better in JS, I started by writing most in JS then switched to Python.

The `./testscripts/` folder contains most individual components of the application to be tested all at once. It is no longer maintained.

The `./nodetest/` folder is for the initial testing of the Audd.io API. It is no longer maintained.

## Some milestones

>Due to the data wire from the Raspberry Pi to the led strip acting as an antenna, and producing random, glitchy, flashing patterns, we decided to replace the  data line as well as the common ground wire with a shielded wire taken from a scrap usb cable, which completely eliminated the display errors, even with a slightly longer wire from the pi to the led strip.

>To adjust for bad colors in the display at some point, we used LED non-linearity compensation with a power vs intensity curve. We used the best tool ever for this: Desmos! [Here's](https://www.desmos.com/calculator/maqayzhvgg) the link to the graph.

## About
This is a repository dedicated to the smart album cover display. 

Running on a Raspberry Pi, this recognizes the live music playing and displays it on a 16x16 grid made with LED strips.

### Usage
Create an Audd.io API Key and place it in `./key`. You can use "test" as the key for up to 10 instances.

After installing all packages, run the following commmand:
```bash
$ python3 run.py
```
If that causes a permissions error, run
```bash
$ sudo python3 run.py
```

To set brightness 10%, run
```bash
$ python3 run.py 10
```

To run in testing mode (no screen), run
```bash
$ python3 run.py test
```

### The Software 

Python script records live audio, then uses the [audd.io](https://audd.io) service for music recognition.

Then sets the pixels to whatever the album cover receives.

Note: `authentication.py` doesn't do anything useful... yet!

### The Hardware

<!-- ![Top](assets/top.jpg) -->
<!-- ![LED](assets/led.jpg) -->

See more at [The Lab](https://thelab.gallery/user/AddisonHenikoff)
