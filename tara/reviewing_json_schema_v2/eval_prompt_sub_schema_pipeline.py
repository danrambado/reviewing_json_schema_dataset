import logging
from tara.lib.pipeline import Pipeline
#from tara.reviewing_json_schema_v2.utils.json_main_arg_parser import extract_main_arguments
# include actions
from tara.reviewing_json_schema_v2.extract_json_reference_action import ExtractJsonReferenceAction
from tara.reviewing_json_schema_v2.eval_actions import EvalAction
import sys
import os
from tara.utils.google_sheet import googleSheet

class EvalPromptSubSchemaPieline(Pipeline):
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
        df2 = df2[['TASK','languageCode', 'internal_id', 'prompt', 'schema','MR_EVAL_SUB_SCHEMA', 'REFERENCED_JSON', 'reference_JSON', 'summary','score_reference','schema_properties','missing_properties','false_properties']]
        df2['languageCode'] = 'en_US'
        self.df=df2

    def format_eval(self):
        df2=self.df

        # keep the columns needed
        df2 = df2[['TASK_ID','summary','score_reference','priority']]
        self.df=df2

    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()
        self.filter_row()

        #First action
        action = EvalAction()
        #action.set_model('o1-mini')
        action.set_model(self.model)
        
        #self.execute_action(action.eval_sub_schema,'MR_EVAL_SUB_SCHEMA')
        #self.execute_action(action.extract_eval_sub_schema,'REFERENCED_JSON')

        action= ExtractJsonReferenceAction()

        self.execute_action(action.extract_referenced_json,'REFERENCED_JSON_FORMATED')
        self.execute_action(action.summary_json,'summary_json')
        self.execute_action(action.summary_format,'summary')

        self.df['score_reference'] = self.df['summary_json'].apply(lambda x: x['score_reference'])
        self.df['schema_properties'] = self.df['summary_json'].apply(lambda x: x['schema_count'])
        self.df['missing_properties'] = self.df['summary_json'].apply(lambda x: x['missing_properties_prompt'])
        self.df['referenced_false'] = self.df['summary_json'].apply(lambda x: x['referenced_false'])
        self.df['referenced_true'] = self.df['summary_json'].apply(lambda x: x['referenced_true'])
        self.df['accuracy'] = self.df['summary_json'].apply(lambda x: x['accuracy'])

        # Create new column Priority with values
        # - 1 if df['score_reference']==1
        # - 2 if df['score_reference']<0.6
        # - 3 if 1<df['score_reference']>=0.6

        self.df['priority'] = self.df['score_reference'].apply(lambda x: 1 if x == 1 else (2 if x < 0.6 else 3))

        # Filter accuracy > 0.9
        self.df=self.df[self.df['accuracy']>0.9]
        self.format_eval()

        # self.format_output()
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
    pipeline.csv_file_input = os.path.join(sys.argv[1], '00_seed.csv')
    # pipeline.csv_file_output = os.path.join(sys.argv[1], 'analysis.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '01_output.csv')
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]

    pipeline.process()

    sheet_id="1W8ZTYjzonvHQs54TcxvdKQE_hau65Mf_nef3iegwfPA"
    # Extract the last folder name 
    last_folder = sys.argv[1].rstrip('/').split('/')[-1]
    # Replace Result in Google sheet
    sheet = googleSheet()
    sheet.from_csv_to_sheet(pipeline.csv_file_output , sheet_id,last_folder)    
