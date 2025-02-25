from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema.summary_actions import SummaryAction
import sys
import os

class SummaryPieline(Pipeline):
    def __init__(self):
        super().__init__()
    
    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()

        #First action
        action = SummaryAction()
        self.execute_action(action.summary,'SUMMARY')
        self.execute_action(action.eval,'EVAL')
        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: uv run -m tara.reviewing_json_schema.eval_prompt_pipeline  <folder> <model>")
        sys.exit(1)

    # Access the parameters
    pipeline= SummaryPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '04_eval_PII_self_contained.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '05_summary.csv')
    pipeline.model = sys.argv[2]


    pipeline.process()
