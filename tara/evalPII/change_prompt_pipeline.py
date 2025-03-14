from tara.lib.pipeline import Pipeline
# include actions
from tara.evalPII.eval_PII_actions import EvalPIIAction

import sys
import os

from tara.utils.google_sheet import googleSheet

class EvalPromptPIISelfContaindedPieline(Pipeline):
    def __init__(self):
        super().__init__()
    
    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()
        #self.df=self.df.sample(2)

        #First action
        print(self.model)
        action = EvalPIIAction()
        action.set_model(self.model)
        self.execute_action(action.change_prompt,'MR_EVAL_PROMPT_PII')
        #self.execute_regex_action(r"<PROMPT_INCLUDE_FULL_NAME>(.*?)</PROMPT_INCLUDE_FULL_NAME>",'MR_EVAL_PROMPT_PII','EVAL_PII',action)       
        self.execute_regex_action(r"<FIXED_PROMPT>(.*?)</FIXED_PROMPT>",'MR_EVAL_PROMPT_PII','FIXED_PROMPT_FULL_NAMES',action)       
        self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'MR_EVAL_PROMPT_PII','EXPLANATION_PII',action)       

        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: uv run -m tara.reviewing_json_schema.eval_prompt_pipeline  <folder> <model>")
        sys.exit(1)

    # Access the parameters
    pipeline= EvalPromptPIISelfContaindedPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '00_L12.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '01_eval.csv')
    pipeline.model = sys.argv[2]


    pipeline.process()
    sheet_id="15SkMV6Frg-4eHuORPAP6Zim9PLxEM5YJzs4bbYZU_c0"
    # Extract the last folder name 
    last_folder = sys.argv[1].rstrip('/').split('/')[-1]
    # Replace Result in Google sheet
    sheet = googleSheet()
    sheet.from_csv_to_sheet(pipeline.csv_file_output , sheet_id,last_folder)