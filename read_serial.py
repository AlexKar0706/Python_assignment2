import datetime
import serial
import time


# Define serial port and baud rate

ser = serial.Serial('COM3', baudrate=500000)
ser.setRTS(False)
ser.setDTR(False)

# Specify the duration to listen (in seconds)
listening_duration = 30 # Change this value to set the duration

# Open a text file for writing
with open("received_data_1703.txt", "w") as file:
	start_time = time.time() # Get the start time
	try:
		# Continuous loop to listen for incoming data until the duration limit is reached
		while time.time() - start_time < listening_duration:
			# Read data from the serial port
			data = ser.readline().decode().strip()
			# Get current timestamp
			timestamp = datetime.datetime.now()
			# Write the received data with timestamp to the text file
			if (data):
				file.write(f"{timestamp}: {data}\n")

	except KeyboardInterrupt:
		# Close the serial port and the text file when Ctrl+C is pressed
		ser.close()
		print("Serial port closed.")
	
