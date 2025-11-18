import bcrypt

password = b"password123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# Verifying
bcrypt.checkpw(password, hashed)  # Returns True
print(password)
print(hashed)