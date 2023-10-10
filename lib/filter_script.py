import os
from datetime import datetime
import pandas as pd

# Specify the input and output directories
input_dir = "csv/"
output_dir = "csv_small/"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each CSV file
csv_files = [file for file in os.listdir(input_dir) if file.endswith(".csv")]

total_files = len(csv_files)
file_count = 0
skipped_files = 0

for csv_file in csv_files:
    file_count += 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the output file already exists
    output_file_path = os.path.join(output_dir, csv_file)
    if os.path.exists(output_file_path):
        skipped_files += 1
        print(
            f"[{file_count}/{total_files}][{timestamp}] Skipping: {csv_file} (already filtered)"
        )
        continue

    # Read the CSV file into a dataframe
    df = pd.read_csv(
        os.path.join(input_dir, csv_file), sep=";", encoding="latin-1", low_memory=False
    )

    # Filtering
    df = (df.ffill()).bfill()
    filtered_df = df.loc[
        (df["NudzBr_1"] == 1)
        | (df["NudzBr_2"] == 1)
        | (df["Zvonec"] == 1)
        | (df["KolBr_1"] == 1)
        | (df["KolBr_2"] == 1)
        | (df["Sklz_Smyk"] == 1)
    ]

    # Save the filtered dataframe to a new CSV file in the output directory
    filtered_df.to_csv(output_file_path, sep=";", encoding="latin-1", index=False)

    print(f"[{file_count}/{total_files}][{timestamp}] Saved:    {csv_file}")
print(f"Finished! Skipped {skipped_files}/{total_files} files (already filtered)")
