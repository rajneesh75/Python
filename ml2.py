import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Example dataset
data = {'experience': [1, 2, 3, 4, 5], 'salary': [30000, 35000, 40000, 45000, 50000]}
df = pd.DataFrame(data)

X = df[['experience']]
y = df['salary']
sns.scatterplot(x='experience', y='salary', data=df)
plt.show()
