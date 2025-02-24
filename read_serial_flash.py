import datetime
import serial
import time


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
                
                # Retrive data
                timestamp = data[:19]
                samples = data[20:].split(",")

                # Send confirmation
                binary_str = bytes("k\n", 'ASCII')
                ser.write(binary_str)

                # Save data
                for sample in samples:
                    file.write(f"{timestamp}: {sample}\n")

    except KeyboardInterrupt:
        # Close the serial port and the text file when Ctrl+C is pressed
        ser.close()
        print("Serial port closed.")
	
ser.close()