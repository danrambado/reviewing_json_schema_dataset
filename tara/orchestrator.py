from tara.reviewing_json_schema.seed_top_layer import SeedTopLayerPieline
from tara.reviewing_json_schema.eval_prompt_pipeline import EvalPromptPieline
from tara.reviewing_json_schema.eval_prompt_sub_schema_pipeline import EvalPromptSubSchemaPieline
from tara.reviewing_json_schema.eval_prompt_PII_self_contained_pipeline import EvalPromptPIISelfContaindedPieline
from tara.reviewing_json_schema.summary_pipeline import SummaryPieline

from tara.utils.google_sheet import googleSheet
import logging
import sys
import os

if len(sys.argv) != 5:
    print("Usage: uv run -m tara.orchestrator <folder> <model> <init_row_number> <end_row_number>")
    sys.exit(1)
# Params
folder=sys.argv[1]
model=sys.argv[2]

# Configure logging
logging.basicConfig(filename=os.path.join(folder,'app.log'), level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == '__main__':
    
    sheet_id='1gDGHiKjlMHJy6pkIWQwKxFGlsc23gcrImpq4BEXJHwM'
    
    # Seed
    pipeline= SeedTopLayerPieline()
    pipeline.csv_file_input = os.path.join(folder, '00_seed.csv')
    file_01=os.path.join(folder, '01_top_layer.csv')
    pipeline.csv_file_output = file_01
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]
    pipeline.process()


    pipeline_seed= EvalPromptPieline()
    pipeline_seed.csv_file_input = file_01
    file_02=os.path.join(folder, '02_eval_top_layer.csv')
    pipeline_seed.csv_file_output = file_02
    pipeline_seed.model = model
    pipeline_seed.init_row_number = sys.argv[3]
    pipeline_seed.end_row_number = sys.argv[4]
    pipeline_seed.process()


    # Access the parameters
    pipeline= EvalPromptSubSchemaPieline()
    pipeline.csv_file_input = file_02
    file_03=os.path.join(folder, '03_eval_sub_schema.csv')
    pipeline.csv_file_output = file_03
    pipeline.model = model
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]
    pipeline.process()    

    # Access the parameters
    pipeline= EvalPromptPIISelfContaindedPieline()
    pipeline.csv_file_input = file_03
    file_04=os.path.join(folder, '04_eval_PII_self_contained.csv')
    pipeline.csv_file_output = file_04
    pipeline.model = model
    pipeline.process()

    pipeline= SummaryPieline()
    pipeline.csv_file_input =file_04
    pipeline.csv_file_output = os.path.join(folder, '05_summary.csv')
    pipeline.process()    

    # Save in GoogleSheet
    # Extract the last folder name 
    last_folder = folder.rstrip('/').split('/')[-1]
    # Replace Result in Google sheet
    sheet = googleSheet()
    sheet.from_csv_to_sheet(pipeline.csv_file_output , sheet_id,last_folder)
