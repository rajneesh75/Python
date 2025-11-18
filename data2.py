import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv')

sns.histplot(df['Salary'])
plt.show()
