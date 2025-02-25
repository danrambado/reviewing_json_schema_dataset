import logging
from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema.eval_actions import EvalAction
import sys
import os

class EvalPromptSubSchemaPieline(Pipeline):
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
        action.set_model('o1-mini')
        self.execute_regex_action(r"<JSON>(.*?)</JSON>",'MR_EVAL_PROMPT_MATCH_JSON','EVAL_PROMPT_MATCH_JSON',action)       
        self.execute_action(action.eval_sub_schema,'MR_EVAL_PROMPT_MATCH_SUB_SCHEMA_JSON')

        self.execute_action(action.extract_eval_sub_schema,'LIST_JSON_EVAL')

        self.execute_action(action.count_prop_fully_referenced,'COUNT_FULLY_REFERENCED_OK')
        self.execute_action(action.count_prop_not_fully_referenced,'COUNT_FULLY_REFERENCED_FAIL')
        self.execute_action(action.count_missing_prop,'COUNT_MISSING_PROP')

        self.execute_action(action.extract_message,'JUSTIFICATION_PROP')

        self.df['PROP_SCORE']=self.df['COUNT_FULLY_REFERENCED_OK']/(self.df['COUNT_FULLY_REFERENCED_OK']+self.df['COUNT_FULLY_REFERENCED_FAIL'])
        # Save the results to a new csv
        self.save_csv()
if len(sys.argv) != 5:
        print("Usage: uv run -m tara.reviewing_json_schema.eval_prompt_sub_schema_pipeline  <folder> <model> <init_row> <end_row>")
        sys.exit(1)
folder = sys.argv[1]
logging.basicConfig(filename=os.path.join(folder,'app.log'), level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == '__main__':
    # Check if the correct number of arguments is provided

    # Access the parameters
    pipeline= EvalPromptSubSchemaPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '02_eval_top_layer.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '03_eval_sub_schema.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()
