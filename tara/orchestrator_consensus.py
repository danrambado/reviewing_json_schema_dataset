from tara.reviewing_json_schema_brutal_force.consensus_pipeline import ConsensusPipeline
from tara.utils.google_sheet import googleSheet
import logging
import sys
import os

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 pipeline.py <file1> <file2> <output>")
        sys.exit(1)
    
    orchestrator=ConsensusPipeline()
    orchestrator.file1=sys.argv[1]
    orchestrator.file2=sys.argv[2]
    orchestrator.output=sys.argv[3]
    orchestrator.process()
    
    sheet_id='1gDGHiKjlMHJy6pkIWQwKxFGlsc23gcrImpq4BEXJHwM'

    # Save in GoogleSheet
    # Extract the last folder name 
    last_folder = orchestrator.output.rstrip('/').split('/')[-2]
    # Replace Result in Google sheet
    sheet = googleSheet()
    sheet.from_csv_to_sheet(orchestrator.output , sheet_id,last_folder)
