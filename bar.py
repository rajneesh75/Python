import matplotlib.pyplot as plt

# Sample data
categories = ['A', 'B', 'C', 'D']
values = [3, 7, 2, 5]

# Creating the bar chart
plt.bar(categories, values)

# Adding title and labels
plt.title('Sample Bar Chart')
plt.xlabel('Categories')
plt.ylabel('Values')

# Display the chart
plt.show()
