e1 = input("Enter name: ")
print(e1)

encoded = e1.encode('utf-8')
print("Encoded Text:", encoded)

for byte in encoded:
    print(hex(byte))

decoded = encoded.decode('utf-8')
print("Decoded Text:", decoded)