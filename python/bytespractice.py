# The prefix 'b' before the quotes means this is a bytes object, not a normal string.
# Bytes are used to store raw binary data such as network packets, files, or encoded text.

data = b'\x41\x42\x43'  # b means bytes instead of normal text (str)

# '\x' represents a hexadecimal (base-16) byte value.
# 0x41 = ASCII value for 'A'
# 0x42 = ASCII value for 'B'
# 0x43 = ASCII value for 'C'

# So the bytes object actually contains the characters: ABC

print(data)

# Accessing index 0 gets the first byte in the bytes object.
# Python starts indexing from 0.
# The first byte is 0x41.

# When accessing a byte using indexing,
# Python returns its decimal integer value.
print(data[0])

# hex() converts the decimal number into hexadecimal format
# hex() converts the decimal integer into hexadecimal format.
# 65 becomes 0x41.
print(hex(data[0]))

# chr() converts the decimal ASCII value into its actual character.
# 65 becomes 'A'.
print(chr(data[0]))

text = "hello"

# encode('utf-8') converts the string into bytes using UTF-8 encoding.
# Computers internally store and transmit data in bytes, not normal text.
encoded = text.encode('utf-8')
# UTF-8 is a standard character encoding format used in:
# - websites
# - networking
# - APIs
# - cybersecurity tools
# - operating systems

# Each character is converted into its byte representation.
# h = 104 decimal = 0x68 hexadecimal
# e = 101 decimal = 0x65 hexadecimal
# l = 108 decimal = 0x6C hexadecimal
# o = 111 decimal = 0x6F hexadecimal

# So:
# "hello"
# becomes:
# b'\x68\x65\x6c\x6c\x6f'


# Printing the encoded variable displays the bytes object.
print(encoded)

# Accessing an index in a bytes object returns the decimal value of that byte.
# encoded[0] gets the first byte: 'h'
# 'h' = 104 in ASCII/UTF-8
print(encoded[0])


# hex() converts the decimal byte value into hexadecimal format.
# 104 becomes 0x68
print(hex(encoded[0]))

# chr() converts the decimal ASCII value back into its character form.
# 104 becomes 'h'
print(chr(encoded[0]))

decoded = encoded.decode('utf-8')
print(decoded)