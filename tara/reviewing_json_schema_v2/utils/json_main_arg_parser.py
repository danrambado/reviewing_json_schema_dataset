import pandas as pd
import json

def extract_main_arguments(json_text):
    """
    Extracts the top-level keys from the 'properties' field of a JSON schema
    while keeping the entire schema structure intact.
    """
    if not isinstance(json_text, str) or json_text.strip() == "":
        return json.dumps({"type": "object", "properties": []})  # Return empty JSON structure

    try:
        schema_dict = json.loads(json_text)  # Convert string to JSON object
        
        # Extract top-level properties
        properties = schema_dict.get("properties", {})
        extracted_keys = list(properties.keys())  # Extract only top-level keys

        # Replace 'properties' field with extracted keys in a list format
        schema_dict["properties"] = extracted_keys  # Keep structure, just modify properties

        return json.dumps(schema_dict, indent=4)  # Return the modified JSON schema as a formatted string

    except json.JSONDecodeError:
        return json.dumps({"type": "object", "properties": []})  # Return default structure in case of error

def main():
    # Load data from CSV file
    df = pd.read_csv("data/generated_training.csv")  # Update with actual file path

    # Check if 'schema' column exists
    if 'schema' not in df.columns:
        raise ValueError("Error: 'schema' column not found in the dataset.")

    # Extract main arguments while keeping the full JSON structure
    df['modified_schema'] = df['schema'].apply(extract_main_arguments)

    # Save the results to a new CSV file (with JSON inside cells)
    csv_output_file = "data/json_parsed_main_arg.csv"
    df.to_csv(csv_output_file, index=False, quoting=1)  # quoting=1 ensures JSON strings are correctly saved

    print(f"Processed data saved to {csv_output_file}")

    return df

if __name__ == "__main__":
    result_df = main()
    print(result_df.head())
