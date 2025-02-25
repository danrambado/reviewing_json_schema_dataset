from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema.eval_actions import EvalAction
import sys
import os
import logging

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
        action = EvalAction()
        action.set_model(self.model)

        self.execute_action(action.eval_match_prompt_json2,'MR_EVAL_MATCH_PROMPT_JSON')
        
        self.execute_regex_action(r"<JSON>(.*?)</JSON>",'MR_EVAL_MATCH_PROMPT_JSON','JSON_RESPONSE',action)
        self.execute_regex_action(r"<FORGOTEN_REQUIRED_PROPERTIES>(.*?)</FORGOTEN_REQUIRED_PROPERTIES>",'MR_EVAL_MATCH_PROMPT_JSON','FORGOTEN_REQUIRED_PROPERTIES',action)
        self.execute_regex_action(r"<FORGOTEN_SELF_CONTAINED_PROPERTIES>(.*?)</FORGOTEN_SELF_CONTAINED_PROPERTIES>",'MR_EVAL_MATCH_PROMPT_JSON','FORGOTEN_SELF_CONTAINED_PROPERTIES',action)
        self.execute_regex_action(r"<EXCESS_PROPERTIES>(.*?)</EXCESS_PROPERTIES>",'MR_EVAL_MATCH_PROMPT_JSON','EXCESS_PROPERTIES',action)
        self.execute_action(action.count_match_properties,'COUNT_MATCH_PROPERTIES')

        #action = EvalSelfContainedAction()
        #action.set_model(self.model)
#
        #self.execute_action(action.eval_self_containded,'ER_EVAL_RESPONSE')
        #
        #self.execute_regex_action(r"<RESPONSE_OK>(.*?)</RESPONSE_OK>",'ER_EVAL_RESPONSE','EVAL_PII',action)
        #self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'ER_EVAL_RESPONSE','JUSTIFICATION_PII',action)

        

        # Save the results to a new csv
        self.save_csv()

if len(sys.argv) != 5:
        print("Usage: uv run -m tara.reviewing_json_schema.eval_prompt_pipeline  <folder> <model> <init_row> <end_row>")
        sys.exit(1)
folder = sys.argv[1]
# Configure logging
logging.basicConfig(filename=os.path.join(folder,'app.log'), level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    
    # Access the parameters
    pipeline= EvalResponsePieline()
    pipeline.csv_file_input = os.path.join(folder, 'seed.csv')
    pipeline.csv_file_output = os.path.join(folder, 'eval.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()
