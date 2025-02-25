from tara.lib.pipeline import Pipeline
# include actions
from tara.reviewing_json_schema.eval_PII_actions import EvalPIIAction
from tara.reviewing_json_schema.eval_selfContained_Action import EvalSelfContainedAction
import sys
import os

class EvalPromptPIISelfContaindedPieline(Pipeline):
    def __init__(self):
        super().__init__()
    
    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()

        #First action
        print(self.model)
        action = EvalPIIAction()
        action.set_model(self.model)
        self.execute_action(action.eval_PII,'MR_EVAL_PROMPT_PII')
        self.execute_regex_action(r"<PROMPT_OK>(.*?)</PROMPT_OK>",'MR_EVAL_PROMPT_PII','EVAL_PII',action)       
        self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'MR_EVAL_PROMPT_PII','EXPLANATION_PII',action)       
        print(self.model)
        action = EvalSelfContainedAction()
        action.set_model(self.model)
        self.execute_action(action.eval_self_containded,'MR_EVAL_PROMPT_SELF_CONTAINED')
        self.execute_regex_action(r"<PROMPT_OK>(.*?)</PROMPT_OK>",'MR_EVAL_PROMPT_SELF_CONTAINED','EVAL_SELF_CONTAINED',action)       
        self.execute_regex_action(r"<EXPLANATION>(.*?)</EXPLANATION>",'MR_EVAL_PROMPT_SELF_CONTAINED','EXPLANATION_SELF_CONTAINED',action)       
        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: uv run -m tara.reviewing_json_schema.eval_prompt_pipeline  <folder> <model>")
        sys.exit(1)

    # Access the parameters
    pipeline= EvalPromptPIISelfContaindedPieline()
    pipeline.csv_file_input = os.path.join(sys.argv[1], '03_eval_sub_schema.csv')
    pipeline.csv_file_output = os.path.join(sys.argv[1], '04_eval.csv')
    pipeline.model = sys.argv[2]


    pipeline.process()
