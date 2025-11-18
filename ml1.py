from sklearn.linear_model import LinearRegression
import pandas as pd

# Example dataset
data = {'experience': [1, 2, 3, 4, 5], 'salary': [30000, 35000, 40000, 45000, 50000]}
df = pd.DataFrame(data)

X = df[['experience']]
y = df['salary']

print(X)
print(y)

model = LinearRegression()
model.fit(X, y)

predicted = model.predict([[6]])
print(predicted)
