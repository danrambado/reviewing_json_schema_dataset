from tara.lib.pipeline import Pipeline
# include actions
import sys
import os
import pandas as pd
import json


class SeedTopLayerPieline(Pipeline):
    def __init__(self):
        super().__init__()
    
    def filter_row(self):
        self.df = self.df.iloc[int(self.init_row_number):int(self.end_row_number)]
        self.console.log(f"Filtering from row {self.init_row_number}  to row {self.end_row_number}")
        self.console.log(f"Total rows: {len(self.df)}")

    def process(self):
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


        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()
        self.filter_row()
        self.df['schema']=self.df['schema'].str.replace("```json","").str.replace("```","").str.strip()
        self.df['modified_schema'] = self.df['schema'].apply(extract_main_arguments)

        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5:
        print("Usage: uv run -m tara.reviewing_json_schema.seed_top_layer  <folder> <model> <init_row> <end_row>")
        sys.exit(1)

    # Access the parameters
    pipeline= SeedTopLayerPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '00_seed.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '01_top_layer.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()
