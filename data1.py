import pandas as pd

df = pd.read_csv('data.csv')
print(df.head())      # show first 5 rows
print(df.info())      # data types and missing values
print(df.describe())  # summary statistics
avg_salary = df['Salary'].mean()

print(avg_salary)