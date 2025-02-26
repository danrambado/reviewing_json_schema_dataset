from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema_brutal_force.generate_response_action import GenerateResponseAction
import sys
import os

class GenerateResponsePieline(Pipeline):
    def __init__(self):
        super().__init__()
    

    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()

        #First action
        action = GenerateResponseAction()
        action.set_model(self.model)

        self.execute_action(action.generate_response,'MR_JSON_RESPONSE')
        self.execute_action(action.extract_json,'JSON_RESPONSE')
        #self.execute_regex_action(r"<JSON_RESPONSE>(.*?)</JSON_RESPONSE>",'MR_JSON_RESPONSE','JSON_RESPONSE',action)       
        
        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: uv run -m tara.reviewing_json_schema_brutal_force.generate_response_pipeline  <folder> <model> <seed/fix>")
        sys.exit(1)

    # Access the parameters
    pipeline= GenerateResponsePieline()
    if sys.argv[3]=='seed':
        pipeline.csv_file_input = os.path.join(sys.argv[1], '01_clean_schema.csv')
    else:
        pipeline.csv_file_input = os.path.join(sys.argv[1], '04_fix_prompt.csv')
    
    pipeline.csv_file_output = os.path.join(sys.argv[1], '02_response.csv')
    pipeline.model = sys.argv[2]

    pipeline.process()
