import pandas as pd
import os

# Define the directory containing the CSV files
directory = 'TORGO_split'

# Function to determine if the text is isolated word or continuous speech
def is_isolated(text):
    return len(text.split()) == 1

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Load the data
        data = pd.read_csv(file_path)

        # Apply the function to create a new column for filtering
        data['is_isolated'] = data['wrd'].apply(is_isolated)

        # Split the data into two DataFrames
        isolated_data = data[data['is_isolated']]
        continuous_data = data[~data['is_isolated']]

        # Drop the temporary column
        isolated_data = isolated_data.drop(columns=['is_isolated'])
        continuous_data = continuous_data.drop(columns=['is_isolated'])

        # Save to new CSV files
        isolated_filename = f'isolated_words_{filename}'
        continuous_filename = f'continuous_speech_{filename}'
        isolated_data.to_csv(os.path.join(directory, isolated_filename), index=False)
        continuous_data.to_csv(os.path.join(directory, continuous_filename), index=False)

        print(f"Processed {filename}:")
        print(f"Saved isolated words to {isolated_filename}")
        print(f"Saved continuous speech to {continuous_filename}")

print("All files have been processed.")

