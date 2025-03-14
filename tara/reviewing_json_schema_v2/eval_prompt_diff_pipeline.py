import logging
from tara.lib.pipeline import Pipeline
#from tara.reviewing_json_schema_v2.utils.json_main_arg_parser import extract_main_arguments
# include actions
from tara.reviewing_json_schema_v2.diff_actions import DiffAction
import sys
import os
from tara.utils.google_sheet import googleSheet

class EvalPromptDiffPieline(Pipeline):
    def __init__(self):
        super().__init__()
    
    def filter_row(self):
        self.df = self.df.iloc[int(self.init_row_number):int(self.end_row_number)]
        self.console.log(f"Filtering from row {self.init_row_number}  to row {self.end_row_number}")
        self.console.log(f"Total rows: {len(self.df)}")

    def format_output(self):
        df2=self.df.rename(columns={'REFERENCED_JSON_FORMATED': 'reference_JSON',
                'INTERNAL_ID':'internal_id',
                'TASK_ID': 'TASK'})

        # keep the columns needed
        df2['languageCode'] = 'en_US'
        df2 = df2[['TASK','languageCode', 'internal_id', 'prompt', 'schema', 'reference_JSON', 'summary','score_reference', 'REFERENCED_JSON','schema_properties','missing_properties','referenced_false','accuracy']]
        
        self.df=df2

    def format_eval(self):
        self.df=self.df[['TASK_ID','ATTEMPT_ID','MR_EVAL_PROMPT_FULL_NAMES_FIXED','EVAL_FULL_NAMES_FIXED','MR_EVAL_PROMPT_PII_FIXED','EVAL_PII_FIXED','MR_EVAL_PROMPT_COMPANY_NAMES_FIXED','EVAL_COMPANY_NAMES_FIXED','EVAL_PII_FIXED_PROMPT','MR_EVAL_SUB_SCHEMA','REFERENCED_JSON','REFERENCED_JSON_FORMATED','summary_json','summary','score_reference','schema_properties','missing_properties','referenced_false','referenced_true','accuracy','priority','diff']]
        # keep the columns needed
        #df2 = df2[['TASK_ID'',''FIXED_PROMPT','ORIGINAL_PROMPT','diff']]

    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()
        #self.filter_row()

        #First action
        action = DiffAction()
        #action.set_model('o1-mini')
                
        # Comment these lines for eval
        self.execute_action(action.eval_diff,'diff')

        #self.df=self.df[self.df['accuracy']>0.9]
        self.format_eval()

        #self.format_output()
        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided

    # Access the parameters
    pipeline= EvalPromptDiffPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '02_eval_prompt.csv')
    # pipeline.csv_file_output = os.path.join(sys.argv[1], 'analysis.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '03_diff.csv')
    pipeline.init_row_number = sys.argv[2]
    pipeline.end_row_number = sys.argv[3]

    pipeline.process()


    sheet_id="15SkMV6Frg-4eHuORPAP6Zim9PLxEM5YJzs4bbYZU_c0"
    sheet_name='L10_eval_fixed_prompt'
    
    last_folder = sys.argv[1].rstrip('/').split('/')[-1]
    # Replace Result in Google sheet
    sheet = googleSheet()
    sheet.from_csv_to_sheet(pipeline.csv_file_output , sheet_id,sheet_name, mode='append')   
