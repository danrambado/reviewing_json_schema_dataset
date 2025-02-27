from tara.lib.pipeline import Pipeline
from tara.prompt_fixer.prompt_fixer_actions import PromptFixer
import sys
import os

class PromptFixerPieline(Pipeline):
    def __init__(self):
        super().__init__()
    
    def filter_row(self):
        self.df = self.df.iloc[int(self.init_row_number):int(self.end_row_number)]
        self.console.log(f"Filtering from row {self.init_row_number}  to row {self.end_row_number}")
        self.console.log(f"Total rows: {len(self.df)}")

    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()
        self.filter_row()

        #First action
        action = PromptFixer()
        action.set_model(self.model)

        self.execute_action(action.prompt_fixer,'MR_FIXED_PROMPT')
        self.execute_regex_action(r"<FIXED_PROMPT>(.*?)</FIXED_PROMPT>",'MR_FIXED_PROMPT','FIXED_PROMPT_V2',action)
        self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'MR_FIXED_PROMPT','CHANGES_EXPLANATION',action)       
        
        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5:
        print("Usage: uv run -m tara.prompt_fixer.prompt_fixer_pipeline <folder> <model> <init_row> <end_row>")
        sys.exit(1)

    # Access the parameters
    pipeline= PromptFixerPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '01_seed.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '02_fixes.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()
