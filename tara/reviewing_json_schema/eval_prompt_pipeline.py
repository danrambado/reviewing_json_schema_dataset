from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema.eval_PII_actions import EvalPIIAction
import sys
import os

class EvalResponsePieline(Pipeline):
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

        #
        action = EvalPIIAction()
        action.set_model(self.model)

        self.execute_action(action.eval_PII,'ER_EVAL_PROMPT')
        
        self.execute_regex_action(r"<PROMPT_OK>(.*?)</PROMPT_OK>",'ER_EVAL_PROMPT','EVAL_PII',action)
        self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'ER_EVAL_PROMPT','JUSTIFICATION_PII',action)

        #action = EvalSelfContainedAction()
        #action.set_model(self.model)
#
        #self.execute_action(action.eval_self_containded,'ER_EVAL_RESPONSE')
        #
        #self.execute_regex_action(r"<RESPONSE_OK>(.*?)</RESPONSE_OK>",'ER_EVAL_RESPONSE','EVAL_PII',action)
        #self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'ER_EVAL_RESPONSE','JUSTIFICATION_PII',action)

        

        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 5:
        print("Usage: uv run -m tara.reviewing_json_schema.eval_prompt_pipeline  <folder> <model> <init_row> <end_row>")
        sys.exit(1)

    # Access the parameters
    pipeline= EvalResponsePieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], 'seed.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], 'eval.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()
