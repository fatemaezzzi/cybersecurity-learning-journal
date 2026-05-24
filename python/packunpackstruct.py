import struct 

p1 = 271005
s1 = struct.pack('>i', p1)
print(s1) 

s2 = struct.unpack('>i', s1)
print(s2)

size = struct.calcsize('>ihs')
print(size)