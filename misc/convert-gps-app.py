import pandas as pd
import argparse

def transform_csv(input_path, output_path):
    # Read the input CSV
    csv = pd.read_csv(input_path, sep=';')

    # Desired columns for output
    desired_columns = [
        'name',
        'battue',  
        'latitude',
        'longitude',
        'horizontalAccuracy',
        'verticalAccuracy',
        'line_offset_x',
        'line_offset_y',
        'number_offset_x',
        'number_offset_y'
    ]

    # Build the output DataFrame
    output = pd.DataFrame()

    for col in desired_columns:
        if col in csv.columns:
            output[col] = csv[col]
        else:
            output[col] = ''

    # Save the transformed CSV
    output.to_csv(output_path, sep=';', index=False)
    print(f"Transformation complete. Output saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform CSV structure to match target format.")
    parser.add_argument("input", help="Path to the input CSV file.")
    parser.add_argument("output", help="Path to save the transformed CSV file.")

    args = parser.parse_args()

    transform_csv(args.input, args.output)
