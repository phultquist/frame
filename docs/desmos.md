# Desmos
Auto brightness is important to keep the user's eyes from hurting, and is generally needed.

With a light sensor we can record the **lux** of the room, which is some unit; but it's kind of arbitrary.

Really, we need to convert the lux to a brighntess value of the LEDs.

## Lux, a runtime variable, needs to be mapped to an optimal brightness between 0 and 1.

#### Let's say lux has a maximum value of `M`

Let's call the mapping function f(x), where f is the output brightness [0,1]

The most basic mapping function would be
```
f(x) = x/M
```

Thus, if the lux is the maximum **M**, the brightness will be 1. 

On the same hand, if the lux is **0** (it's minimum), the brightness will be 0. 

Of course, this won't work. If the brightneess is 0, the screen would be off. 

## Thus, we need to find this function `f(x)`

