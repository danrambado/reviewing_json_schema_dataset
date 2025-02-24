from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema.eval_actions import EvalAction
import sys
import os

class EvalPromptPieline(Pipeline):
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
        action = EvalAction()
        action.set_model(self.model)

        self.execute_action(action.eval_sub_schema,'MR_EVAL_PROMPT_MATCH_SUB_SCHEMA_JSON')

        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5:
        print("Usage: uv run -m tara.reviewing_json_schema.eval_prompt_pipeline  <folder> <model> <init_row> <end_row>")
        sys.exit(1)

    # Access the parameters
    pipeline= EvalPromptPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], 'seed.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], 'eval.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()
