import pandas as pd

for chunk in pd.read_csv("customers-100.csv", chunksize=10):
    print(chunk)
    print("----- End of Chunk -----")
