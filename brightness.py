def get_output_brightness(user_brightness, sensor_value, max_brightness, min_brightness):
	if sensor_value < 0:
            sensor_value = 0
			
	interpreted = sensor_value / 45

	if interpreted > 1:
		interpreted = 1

	# just average the 2
	output_brightness = (interpreted + user_brightness) / 2

	# this is some version of point slope form
	output_brightness = output_brightness * (max_brightness - min_brightness) + min_brightness

	return output_brightness