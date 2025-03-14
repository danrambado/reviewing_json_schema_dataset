from tara.reviewing_json_schema_v2.eval_prompt_PII_pipeline import EvalPromptPIIPieline
from tara.reviewing_json_schema_v2.eval_prompt_diff_pipeline import EvalPromptDiffPieline
from tara.reviewing_json_schema_v2.eval_prompt_sub_schema_pipeline import EvalPromptSubSchemaPieline
from tara.reviewing_json_schema_v2.extract_redash_filter_last_attempt import ExtractRedashFilter_Last_Attempt
from tara.utils.google_sheet import googleSheet
import logging
import sys
import os

if len(sys.argv) != 3:
    print("Usage: uv run -m tara.orchestrator <folder> <model>")
    sys.exit(1)
# Params
folder=sys.argv[1]
model=sys.argv[2]

# Configure logging
logging.basicConfig(filename=os.path.join(folder,'app.log'), level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == '__main__':
    
    sheet_id="15SkMV6Frg-4eHuORPAP6Zim9PLxEM5YJzs4bbYZU_c0"
    sheet_name='L10_eval_fixed_prompt'

    pipeline= ExtractRedashFilter_Last_Attempt()
    pipeline.folder = os.path.join(folder)
    pipeline.csv_file_redash = os.path.join(folder, '00_redash.csv')
    pipeline.csv_file_sheet = os.path.join(folder, '00_sheet.csv')
    pipeline.csv_file_input = os.path.join(folder, '00_redash.csv')
    pipeline.csv_file_output = os.path.join(folder, '00_seed.csv')

    pipeline.sheet_id=sheet_id
    pipeline.sheet_name=sheet_name

    pipeline.process()    

    # Access the parameters
    pipeline= EvalPromptPIIPieline()
    pipeline.csv_file_input = os.path.join(folder, '00_seed.csv')
    pipeline.csv_file_output = os.path.join(folder, '01_eval_PII.csv')
    pipeline.model = model
    pipeline.process()

    # Access the parameters
    pipeline= EvalPromptSubSchemaPieline()
    pipeline.csv_file_input = os.path.join(folder, '01_eval_PII.csv')
    pipeline.csv_file_output = os.path.join(folder, '02_eval_prompt.csv')
    pipeline.model = model

    pipeline.process()

    # Access the parameters
    pipeline= EvalPromptDiffPieline()
    pipeline.csv_file_input = os.path.join(folder, '02_eval_prompt.csv')
    pipeline.csv_file_output = os.path.join(folder, '03_diff.csv')

    pipeline.process()

    # Append Result in Google sheet
    sheet = googleSheet()
    sheet.from_csv_to_sheet(pipeline.csv_file_output , sheet_id,sheet_name, mode='append')   
