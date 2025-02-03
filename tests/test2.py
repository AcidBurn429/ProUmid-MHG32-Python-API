from ctypes import c_uint32 as unsigned_int32
import struct


return_value = b'\x01\x03\x14\x01g\x01\x17\x80\x00\x80\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\xd8\x9c'

converted_data = bytearray(return_value).hex()

data = int(converted_data[6:-12], 16)

unsigned_data = unsigned_int32(data)

exponent = (unsigned_data.value & 0x00000000000000FF) << 16
sign_bits = (unsigned_data.value & 0x000000000000FF00) << 16
mantissa = unsigned_data.value >> 16

bin_final_float = (sign_bits | exponent) | mantissa
current_temperature = struct.unpack('!f', bin_final_float.to_bytes(4, byteorder='big'))[0]  # Current temperature
print("[Humidity] --> Current Temperature: {}°C".format(round(current_temperature, 2)))
