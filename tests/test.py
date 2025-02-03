from ctypes import c_uint32 as unsigned_int32
import struct

return_value = b'\x01\x03\x14\x01g\x01\x17\x80\x00\x80\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\xd8\x9c'
converted_data = bytearray(return_value).hex()
#print(return_value[3:21])
data = int(converted_data[3:21], 16)
unsigned_data = unsigned_int32(data)
print(unsigned_data)
#float(return_value[3:21])
current_temperature = struct.unpack('>d', return_value[3:22])[0]  # Current temperature

print(current_temperature)
