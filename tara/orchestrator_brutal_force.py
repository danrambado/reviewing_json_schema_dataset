from tara.reviewing_json_schema_brutal_force.clean_filter_pipeline import CleanFilterPieline
from tara.reviewing_json_schema_brutal_force.eval_orchestrator import EvalOrchstrator

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
    pipeline= CleanFilterPieline()
    pipeline.csv_file_input = os.path.join(folder, '00_seed.csv')
    file_01=os.path.join(folder, '01_clean_schema.csv')
    pipeline.csv_file_output = file_01
    pipeline.model = sys.argv[2]
    pipeline.init_row_number = sys.argv[3]
    pipeline.end_row_number = sys.argv[4]
    pipeline.process()


    pipeline_eval= EvalOrchstrator()
    pipeline_eval.folder =folder
    pipeline_eval.model = model
    pipeline_eval.process()

    # Save in GoogleSheet
    # Extract the last folder name 
    last_folder = folder.rstrip('/').split('/')[-1]
    # Replace Result in Google sheet
    sheet = googleSheet()
    sheet.from_csv_to_sheet(pipeline_eval.csv_file_output , sheet_id,last_folder)
