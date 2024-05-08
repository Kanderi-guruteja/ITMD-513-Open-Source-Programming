import requests
import pandas as pd
import matplotlib.pyplot as plt

# Base URL for Chicago Open Data Portal crime API; plus adding date and location filters
baseurl = "https://data.cityofchicago.org/resource/w98m-zvie.json"
datebetw = "?$where=date between '2019-01-01T12:00:00' and '2019-07-16T14:00:00'"
boxurl = 'within_box(location, 41.975121, -87.791649, 41.978260, -87.763931)'
ourl = baseurl + datebetw + ' AND ' + boxurl

response = requests.get(ourl)
data = response.json()

# Create a pandas DataFrame from the retrieved data
df = pd.DataFrame(data, columns=['date', 'block', 'primary_type', 'description'])

# Convert the 'date' column to pandas datetime format
df['date'] = pd.to_datetime(df['date'])

# Convert other columns to categorical type (not numeric)
df['block'] = df['block'].astype('category')
df['primary_type'] = df['primary_type'].astype('category')
df['description'] = df['description'].astype('category')

# Print the DataFrame to verify the data retrieval and conversions
print(df.head())

# Additional data analysis
# Descriptive statistics for the 'date' column
numerical_stats = df.describe(include='datetime64')

# Display the summary of descriptive statistics for the 'date' column
print("\nSummary of Descriptive Statistics for 'date' column:")
print(numerical_stats)

# Count unique values in 'block', 'primary_type', and 'description' columns
block_counts = df['block'].value_counts()
primary_type_counts = df['primary_type'].value_counts()
description_counts = df['description'].value_counts()

# Display the counts of unique values in each column
print("\nNumber of unique values in 'block' column:")
print(block_counts)
print("\nNumber of unique values in 'primary_type' column:")
print(primary_type_counts)
print("\nNumber of unique values in 'description' column:")
print(description_counts)



# Create bar plots for 'block', 'primary_type', and 'description'
plt.figure(figsize=(12, 6))

# Plot 'block' data
plt.subplot(1, 3, 1)
block_counts.plot(kind='bar')
plt.title('Block')
plt.xlabel('Block Names')
plt.ylabel('Frequency')

# Plot 'primary_type' data
plt.subplot(1, 3, 2)
primary_type_counts.plot(kind='bar')
plt.title('Primary Type')
plt.xlabel('Crime Types')
plt.ylabel('Frequency')

# Plot 'description' data
plt.subplot(1, 3, 3)
description_counts.plot(kind='bar')
plt.title('Description')
plt.xlabel('Crime Descriptions')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


# Count occurrences of each crime type
primary_type_counts = df['primary_type'].value_counts()

# Display the number of occurrences of each crime type
print("\nNumber of occurrences of each crime type:")
print(primary_type_counts)

# Summary of descriptive statistics for 'primary_type' column
primary_type_descriptive_stats = df['primary_type'].describe()

# Display the summary statistics for 'primary_type' column
print("\nSummary of Descriptive Statistics for 'primary_type' column:")
print(primary_type_descriptive_stats)

# Create a bar plot for 'primary_type' data
plt.figure(figsize=(10, 6))
primary_type_counts.plot(kind='bar')
plt.title('Number of Occurrences of Each Crime Type')
plt.xlabel('Crime Types')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


