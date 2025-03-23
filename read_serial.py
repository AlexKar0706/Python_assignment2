import datetime
import serial
import time
import struct


# Define serial port and baud rate

ser = serial.Serial('COM3', baudrate=500000)
ser.setRTS(False)
ser.setDTR(False)

# Specify the duration to listen (in seconds)
listening_duration = 30 # Change this value to set the duration

def find_start_sequence():
    """Synchronizes by looking for two consecutive start bytes."""
    while True:
        byte1 = ser.read(1)
        if byte1 == b'\xAA':  # First sync byte detected
            byte2 = ser.read(1)
            if byte2 == b'\xFF':  # Second sync byte detected
                #print("Start sequence detected!")
                return True


# Open a text file for writing
with open("received_data_uart.txt", "w") as file:
	start_time = time.time() # Get the start time
	try:
		# Read data from the serial port
		while time.time() - start_time < listening_duration:
			ser.reset_input_buffer()
			if find_start_sequence():
				received_data = ser.read(512)

				if len(received_data) == 512:

					# Get current timestamp
					timestamp = datetime.datetime.now()

					# Write the received data with timestamp to the text file
					for i in range(0, len(received_data), 2):

						int_value = struct.unpack("<h", received_data[i:i+2])[0]						
						file.write(f"{timestamp}: {int_value}\n")
				else:
					print(f"Incomplete data received: {len(received_data)} bytes")

	except KeyboardInterrupt:
		# Close the serial port and the text file when Ctrl+C is pressed
		ser.close()
		print("Serial port closed.")
	
