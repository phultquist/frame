light_sensor_value = 27
magic_brightness_scale_factor = 0.02
user_brightness = 0.5
min_brightness = 0.07
max_brightness = 0.6

if light_sensor_value < (min_brightness / magic_brightness_scale_factor):
	light_sensor_value = (min_brightness / magic_brightness_scale_factor)
if light_sensor_value > (max_brightness / magic_brightness_scale_factor):
	light_sensor_value = (max_brightness / magic_brightness_scale_factor)
output_brightness = light_sensor_value * (0.116 * (74 ** user_brightness)) * magic_brightness_scale_factor
print(output_brightness)
print(0.116 * (74 ** user_brightness))
if output_brightness < min_brightness :
	output_brightness = min_brightness
if output_brightness > max_brightness :
	output_brightness = max_brightness
print(output_brightness)
