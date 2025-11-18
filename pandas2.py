import pandas as pd

data = {
    'Name': ['Raj', 'Amit', 'Priya', 'Neha'],
    'Age': [28, 25, 30, 27],
    'City': ['Delhi', 'Mumbai', 'Pune', 'Chennai']
}

df = pd.DataFrame(data)
print(df)

print(df['Name'])
print(df[['Name', 'City']])


