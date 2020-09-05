light_sensor_value = 27
brightness_scale_factor = 0.02
user = 1.0
min_brightness = 0.07
max_brightness = 0.6


def get_output_brightness(user_brightness, sensor_value):
	if sensor_value < (min_brightness / brightness_scale_factor):
		sensor_value = (min_brightness / brightness_scale_factor)
	if sensor_value > (max_brightness / brightness_scale_factor):
		sensor_value = (max_brightness / brightness_scale_factor)

	output_brightness = sensor_value * (0.116 * (74 ** user_brightness)) * brightness_scale_factor
	if output_brightness < min_brightness:
		output_brightness = min_brightness
	if output_brightness > max_brightness:
		output_brightness = max_brightness
	return output_brightness

print(get_output_brightness(user, light_sensor_value))