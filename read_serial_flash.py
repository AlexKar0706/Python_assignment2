import datetime
import serial
import time
import struct


# Define serial port and baud rate

ser = serial.Serial('COM3', baudrate=500000)
ser.setRTS(False)
ser.setDTR(False)

# Open a text file for writing
with open("received_data_flash.txt", "w") as file:
    try:
        # Continuous loop to listen for incoming data until the duration limit is reached
        while 1:
            # Read data from the serial port
            data = ser.readline().decode().strip()

            # Write the received data with timestamp to the text file
            if (data):

                # Check message type
                if (data[0] == 's'):
                    binary_str = bytes("s\n", 'ASCII')
                    ser.write(binary_str)
                    continue
                elif (data[0] == 'e'):
                    break
                    
                mic_raw_data = ser.read(512)
                
                if len(mic_raw_data) == 512:

                    # Send confirmation
                    binary_str = bytes("k\n", 'ASCII')
                    ser.write(binary_str)

                    # Get current timestamp
                    timestamp = data[:19]

					# Write the received data with timestamp to the text file
                    for i in range(0, len(mic_raw_data), 2):

                        sample = struct.unpack("<h", mic_raw_data[i:i+2])[0]						
                        file.write(f"{timestamp}: {sample}\n")
                else:
                    print(f"Incomplete data received: {len(mic_raw_data)} bytes")

    except KeyboardInterrupt:
        # Close the serial port and the text file when Ctrl+C is pressed
        ser.close()
        print("Serial port closed.")
	
ser.close()