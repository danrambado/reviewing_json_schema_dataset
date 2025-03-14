from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema_v2.eval_PII_actions import EvalPIIAction
import sys
import os

class EvalPromptPIIPieline(Pipeline):
    def __init__(self):
        super().__init__()
    
    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()
        #self.df=self.df.sample(3)
        #First action
        action = EvalPIIAction()
        action.set_model(self.model)
        action.set_origin_column_name('ORIGINAL_PROMPT')

        #self.execute_action(action.eval_full_names,'MR_EVAL_PROMPT_FULL_NAMES')
        #self.execute_regex_action(r"<PROMPT_INCLUDE_FULL_NAMES>(.*?)</PROMPT_INCLUDE_FULL_NAMES>",'MR_EVAL_PROMPT_FULL_NAMES','EVAL_FULL_NAMES',action)       

        #self.execute_action(action.eval_PII,'MR_EVAL_PROMPT_PII')
        #self.execute_regex_action(r"<PROMPT_INCLUDE_PII>(.*?)</PROMPT_INCLUDE_PII>",'MR_EVAL_PROMPT_PII','EVAL_PII',action)       
        #self.execute_action(action.eval_company_names,'MR_EVAL_PROMPT_COMPANY_NAMES')
        #self.execute_regex_action(r"<PROMPT_INCLUDE_COMPANY_NAMES>(.*?)</PROMPT_INCLUDE_COMPANY_NAMES>",'MR_EVAL_PROMPT_COMPANY_NAMES','EVAL_COMPANY_NAMES',action)       
        #self.execute_action(action.eval_original_prompt,'EVAL_PII_ORIGINAL_PROMPT')

        #self.df['MATCH_PII']=self.df['EVAL_PII_ORIGINAL_PROMPT']==self.df['PROMPT_PII']


        action.set_origin_column_name('FIXED_PROMPT')
        self.execute_action(action.eval_full_names,'MR_EVAL_PROMPT_FULL_NAMES_FIXED')
        self.execute_regex_action(r"<PROMPT_INCLUDE_FULL_NAMES>(.*?)</PROMPT_INCLUDE_FULL_NAMES>",'MR_EVAL_PROMPT_FULL_NAMES_FIXED','EVAL_FULL_NAMES_FIXED',action)       
        self.execute_action(action.eval_PII,'MR_EVAL_PROMPT_PII_FIXED')
        self.execute_regex_action(r"<PROMPT_INCLUDE_PII>(.*?)</PROMPT_INCLUDE_PII>",'MR_EVAL_PROMPT_PII_FIXED','EVAL_PII_FIXED',action)       
        self.execute_action(action.eval_company_names,'MR_EVAL_PROMPT_COMPANY_NAMES_FIXED')
        self.execute_regex_action(r"<PROMPT_INCLUDE_COMPANY_NAMES>(.*?)</PROMPT_INCLUDE_COMPANY_NAMES>",'MR_EVAL_PROMPT_COMPANY_NAMES_FIXED','EVAL_COMPANY_NAMES_FIXED',action)       
        self.execute_action(action.eval_fixed_prompt,'EVAL_PII_FIXED_PROMPT')

        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: uv run -m tara.reviewing_json_schema_v2.eval_prompt_PII_pipeline  <folder> <model>")
        sys.exit(1)

    # Access the parameters
    pipeline= EvalPromptPIIPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '00_seed.csv')
    #pipeline.csv_file_input = os.path.join(sys.argv[1], '01_eval_PII.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '01_eval_PII.csv')
    pipeline.model = sys.argv[2]


    pipeline.process()
