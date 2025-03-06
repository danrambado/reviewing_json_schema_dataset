import logging
from tara.lib.pipeline import Pipeline
from tara.reviewing_json_schema_v2.utils.json_main_arg_parser import extract_main_arguments
# include actions
from tara.reviewing_json_schema_v2.eval_actions import EvalAction
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
        #action.set_model('o1-mini')
        action.set_model(self.model)
        
        self.execute_action(action.eval_sub_schema,'MR_EVAL_SUB_SCHEMA')
        self.execute_action(action.extract_eval_sub_schema,'REFERENCED_JSON')
        self.df['SCHEMA_SIMPLIFIED'] = self.df['schema'].apply(extract_main_arguments)
        self.execute_action(action.format_json,'REFERENCED_JSON_FORMATED')





        # self.execute_action(action.count_prop_fully_referenced,'COUNT_FULLY_REFERENCED_OK')
        # self.execute_action(action.count_prop_not_fully_referenced,'COUNT_FULLY_REFERENCED_FAIL')
        # self.execute_action(action.count_missing_prop,'COUNT_MISSING_PROP')

        # self.execute_action(action.extract_message,'JUSTIFICATION_PROP')

        # self.df['PROP_SCORE']=self.df['COUNT_FULLY_REFERENCED_OK']/(self.df['COUNT_FULLY_REFERENCED_OK']+self.df['COUNT_FULLY_REFERENCED_FAIL'])
        
        # Save the results to a new csv
        self.save_csv()
if len(sys.argv) != 5:
        print("Usage: uv run -m tara.reviewing_json_schema_v2.eval_prompt_sub_schema_pipeline  <folder> <model> <init_row> <end_row>")
        sys.exit(1)
folder = sys.argv[1]
logging.basicConfig(filename=os.path.join(folder,'app.log'), level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == '__main__':
    # Check if the correct number of arguments is provided

    # Access the parameters
    pipeline= EvalPromptSubSchemaPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '00_seed_100_200.csv')
    # pipeline.csv_file_output = os.path.join(sys.argv[1], 'analysis.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '01_output_100_200.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()
