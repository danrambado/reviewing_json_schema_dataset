import os
import sys
import pandas as pd
from tara.utils.redash import Redash
from tara.lib.pipeline import Pipeline

class ExtractRedashFilter(Pipeline):

    def filter(self):

        # filtering all the rows in df that are not in df_all_task (join by document_url and table_page_1)

        # Filter rows based on column: 'SUMMARY'
        self.df = self.df[self.df['SUMMARY'].str.contains("Number of Properties", regex=False, na=False, case=False)]
        # Filter rows based on column: 'REFERENCE_JSON'
        self.df = self.df[self.df['REFERENCE_JSON'].notna()]
        # Rename columns
        self.df = self.df.rename(columns={
            'SCHEMA': 'schema',
            'REFERENCE_JSON': 'REFERENCED_JSON'
        })

        self.console.log(f"Total filter rows: {len(self.df)}")


      

    def process(self):
        redash= Redash()
        redash.folder = self.folder
        redash.file_name= self.csv_file_redash
        redash.query_id = "214831"
        redash.process()

        self.read_csv()
        
        self.filter()

        self.save_csv()  



if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("""Usage: uv run -m tara.reviewing_json_schema_v2.extract_redash_filter  <folder> """)
        sys.exit(1)

    # Access the parameters
    pipeline= ExtractRedashFilter()
    pipeline.folder = os.path.join(sys.argv[1])
    pipeline.csv_file_input = os.path.join(sys.argv[1], '00_redash.csv')
    pipeline.csv_file_redash = os.path.join(sys.argv[1], '00_redash.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '00_seed.csv')

    pipeline.process()    
