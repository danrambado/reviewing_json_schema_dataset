import os
import sys
import pandas as pd
from tara.utils.redash import Redash
from tara.utils.google_sheet import googleSheet
from tara.lib.pipeline import Pipeline

class ExtractRedashFilter_Last_Attempt(Pipeline):

    def filter(self):

        # Filter rows based on column: 'SUMMARY'
        self.df = self.df[self.df['FIXED_PROMPT'].notna()]
        # Read sheet
        self.df_sheet=pd.read_csv(self.csv_file_sheet)

        # Filter all rows in self.df where the ATTEMPT_ID is not in self.df_sheet
        self.df = self.df[~self.df['ATTEMPT_ID'].isin(self.df_sheet['ATTEMPT_ID'])]

        self.console.log(f"Total filter rows: {len(self.df)}")
      

    def process(self):
        redash= Redash()
        redash.folder = self.folder
        redash.file_name= self.csv_file_redash
        redash.query_id = "210389" #Last Attempt
        redash.params={"project_id":"67b7fd86f75fa8e311b1c1dc","review_level":"10"}
        redash.process()


        # Replace Result in Google sheet
        sheet = googleSheet()
        sheet.from_sheet_to_csv(self.sheet_id, self.sheet_name, self.csv_file_sheet)

        
        self.read_csv()
        
        self.filter()

        self.save_csv()  



if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("""Usage: uv run -m tara.reviewing_json_schema_v2.extract_redash_filter  <folder> """)
        sys.exit(1)

    # Access the parameters
    pipeline= ExtractRedashFilter_Last_Attempt()
    pipeline.folder = os.path.join(sys.argv[1])
    pipeline.csv_file_input = os.path.join(sys.argv[1], '00_redash.csv')
    pipeline.csv_file_redash = os.path.join(sys.argv[1], '00_redash.csv')
    pipeline.csv_file_sheet = os.path.join(sys.argv[1], '00_sheet.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '00_seed.csv')

    pipeline.sheet_id="15SkMV6Frg-4eHuORPAP6Zim9PLxEM5YJzs4bbYZU_c0"
    pipeline.sheet_name='L10_eval_fixed_prompt'

    pipeline.process()    
