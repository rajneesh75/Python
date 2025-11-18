data = bytearray(b"Python")
view = memoryview(data)
print(view[0])  # 80 (ASCII of 'P')
view[0] = 112  # Change 'P' to 'p'
print(data)
