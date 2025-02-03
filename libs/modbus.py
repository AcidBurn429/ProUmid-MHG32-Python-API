from serial import Serial, SerialException, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
from crc import Calculator, Crc16
from ctypes import c_uint32 as unsigned_int32
import struct
from time import sleep


class Modbus:
    def __init__(self, port: str, modbus_address: int, baudrate: int = 38400,
                 bytesize: int = EIGHTBITS, parity: int = PARITY_NONE,
                 stopbits: int = STOPBITS_ONE):

        self.ser: Serial = Serial(port, baudrate, bytesize=bytesize,
                                  parity=parity, stopbits=stopbits)

        self.modbus_address = modbus_address

        self.CRC_calculator = Calculator(Crc16.MODBUS, optimized=True)

    def _calculateCRC(self, data: bytes):
        checksum: int = self.CRC_calculator.checksum(data)
        bytes_checksum: list = list(checksum.to_bytes(2, 'big'))
        new = bytes([bytes_checksum[1], bytes_checksum[0]])
        return new[1], new[0]

    def _convertToFloat(self, data):
        converted_data = bytearray(data).hex()

        data = int(converted_data[6:-12], 16)

        unsigned_data = unsigned_int32(data)

        exponent = (unsigned_data.value & 0x00000000000000FF) << 16
        sign_bits = (unsigned_data.value & 0x000000000000FF00) << 16
        mantissa = unsigned_data.value >> 16

        bin_final_float = (sign_bits | exponent) | mantissa
        current_temperature = struct.unpack('!f', bin_final_float.to_bytes(4, byteorder='big'))[
            0]  # Current temperature

    def read_register_value(self, address):
        address = list(address)
        request = bytearray([self.modbus_address, 0x03, address[0], address[1], 0x00, 0x20])
        crc = self._calculateCRC(request)
        request.append(crc[1])
        request.append(crc[0])

        packet = bytearray(request)

        self.ser.write(packet)  # Send the request

        sleep(1)
