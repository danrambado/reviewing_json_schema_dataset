from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema_brutal_force.fix_prompt_action import FixPromptAction
import sys
import os

class FixPromptPieline(Pipeline):
    def __init__(self):
        super().__init__()
    

    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()

        #First action
        action = FixPromptAction()
        action.set_model(self.model)

        self.execute_action(action.fix_prompt,'MR_FIX_PROMPT')
        self.execute_regex_action(r"<NEW_PROMPT>(.*?)</NEW_PROMPT>",'MR_FIX_PROMPT','NEW_PROMPT',action)
        self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'MR_FIX_PROMPT','EXPLANATION_FIXED_PROMPT',action)       

        self.df['HISTORY_MR_VALIDATE_RESPONSE']=self.df['MR_VALIDATE_RESPONSE']
        self.df['HISTORY_JSON_RESPONSE']=self.df['JSON_RESPONSE']
        
        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: uv run -m tara.reviewing_json_schema_brutal_force.fix_prompt_pipeline  <folder> <model>")
        sys.exit(1)

    # Access the parameters
    pipeline= FixPromptPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '03_validate.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '04_fix_prompt.csv')
    pipeline.model = sys.argv[2]

    pipeline.process()
