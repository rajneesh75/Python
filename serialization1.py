import pickle

data = {'name': 'Rajneesh', 'role': 'IT Professional'}

# Serialize (object → bytes)
serialized = pickle.dumps(data)
print(serialized)

# Deserialize (bytes → object)
restored = pickle.loads(serialized)

print(restored)