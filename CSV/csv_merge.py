import os
import pandas as pd
import logging as log

# Set up logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define paths
csv_path = r'C:\Users\admin\OneDrive\바탕 화면\cmmsg_2025-01-24\LGCNS자료'
result_path = r'C:\Users\admin\OneDrive\바탕 화면\cmmsg_2025-01-24\결과'
result_file = os.path.join(result_path, 'merged_result.csv')

# Create result directory if it doesn't exist
os.makedirs(result_path, exist_ok=True)

# Initialize a list to store DataFrames
data_frames = []

# Read all CSV files in the directory
for file_name in os.listdir(csv_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_path, file_name)
        df = pd.read_csv(file_path)
        data_frames.append(df)
        log.info(f"Read {file_name} with {len(df)} rows")

# Concatenate all DataFrames
merged_df = pd.concat(data_frames, ignore_index=True)
log.info(f"Merged DataFrame with {len(merged_df)} rows")

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(result_file, index=False)
log.info(f"Saved merged DataFrame to {result_file}")