import pandas as pd

# Load the CSV file
df = pd.read_csv('TORGO_dysarthric_train.csv')

# Drop duplicates
df.drop_duplicates(inplace=True)

# Save the cleaned data to a new CSV file
df.to_csv('TORGO_dysarthric_train_new.csv', index=False)


