from serial import Serial, SerialException, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
from time import sleep
from ctypes import c_uint32 as unsigned_int32
import struct
from threading import Thread

"""
    This class controls the Temperature Chamber
"""


class HumidityChamber(Thread):
    def __init__(self, port, baudrate=38400, bytesize=EIGHTBITS, parity=PARITY_NONE,
                 stopbits=STOPBITS_ONE, verbose=True):
        super().__init__()

        self.port = port  # Port of the device
        self.baudrate = baudrate  # Baud rate with device

        # Do only change if really necessary
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.verbose = verbose

        self.current_temperature = 0.0  # Define the temperature variable

        self._stopper = False  # Variable to stop the Thread

    def get_current_temperature(self):
        """ This function returns the current temperature measured by the device """
        return self.current_temperature

    def run(self) -> None:
        """ This function has to be run to read out the temperature """
        try:
            with Serial(self.port, self.baudrate, bytesize=self.bytesize,
                        parity=self.parity, stopbits=self.stopbits) as ser:

                # As soon as the the program is not closed via the close function repeated
                while not self._stopper:
                    if self.verbose: print("[Temperature] --> Requesting data")

                    # Requesting data from the controller
                    request = [0x01, 0x03, 0x01, 0x21, 0x00, 0x0A, 0x94, 0x3B]  # Bytesequence for requesting the current temperature
                    packet = bytearray(request)

                    ser.write(packet)  # Send the request

                    sleep(1)
                    if self.verbose: print("[Humidity] --> Data received!")
                    return_value: bytes = ser.read(25)  # Receive the response
                    print(return_value)

                    # Convert the transmitted float format into the standard IEEE 754 format
                    converted_data = bytearray(return_value).hex()

                    data = int(converted_data[6:-12], 16)

                    unsigned_data = unsigned_int32(data)

                    exponent = (unsigned_data.value & 0x00000000000000FF) << 16
                    sign_bits = (unsigned_data.value & 0x000000000000FF00) << 16
                    mantissa = unsigned_data.value >> 16

                    bin_final_float = (sign_bits | exponent) | mantissa
                    current_temperature = struct.unpack('!f', bin_final_float.to_bytes(4, byteorder='big'))[
                        0]  # Current temperature
                    if self.verbose: print(
                        "[Humidity] --> Current Temperature: {}°C".format(round(current_temperature, 2)))
                    self.current_temperature = round(current_temperature, 2)

                    sleep(1)

        except SerialException:
            if self.verbose: print("[Temperature] --> Error: Can't connect to the controller!")

    def close(self):
        """This function needs to be called to close the Thread properly."""
        self._stopper = True


chamber = HumidityChamber('COM9', 9600, 8)
chamber.run()
