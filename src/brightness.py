def get_output_brightness(user_brightness, sensor_value, max_brightness, min_brightness):
	if sensor_value < 0:
            sensor_value = 0
	
	interpreted = sensor_value * 4.5	

	

	# multiply interpreted by linear user_brightness value from 0 to 2
	output_brightness = ((user_brightness / 50) * interpreted)
	

	# this is some version of point slope form
	#output_brightness = output_brightness * (max_brightness - min_brightness) + min_brightness

	return output_brightness
