from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema_brutal_force.validate_response_action import ValidateResponseAction
import sys
import os

class ValidateResponsePieline(Pipeline):
    def __init__(self):
        super().__init__()
    

    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()

        #First action
        action = ValidateResponseAction()

        self.execute_action(action.validate_response,'MR_VALIDATE_RESPONSE')
        self.df['VALIDATE_RESPONSE']=self.df['MR_VALIDATE_RESPONSE'].apply(lambda x: x['validate'])
        self.df['ERROR_MESSAGE']=self.df['MR_VALIDATE_RESPONSE'].apply(lambda x: x['error_message'])
        self.df['ERROR_CODE']=self.df['MR_VALIDATE_RESPONSE'].apply(lambda x: x['error_code'])
   
        
        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: uv run -m tara.reviewing_json_schema_brutal_force.validate_response_pipeline  <folder> ")
        sys.exit(1)

    # Access the parameters
    pipeline= ValidateResponsePieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '02_response.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '03_validate.csv')

    pipeline.process()
