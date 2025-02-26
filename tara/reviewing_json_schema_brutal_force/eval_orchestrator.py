from tara.reviewing_json_schema_brutal_force.generate_response_pipeline import GenerateResponsePieline
from tara.reviewing_json_schema_brutal_force.validate_response_pipeline import ValidateResponsePieline
from tara.reviewing_json_schema_brutal_force.fix_prompt_pipeline import FixPromptPieline
import pandas as pd
import sys
import os

class EvalOrchstrator():
    def __init__(self):
        pass

    def process(self):
        # Eval the MODEL RESPONSE with the RUBRIC.
        # If the response answer the RUBRIC generate new PROMPT/RUBRIC/RESPONSE
        df_ok=[]
        counter_fixes=0
        fix_file=os.path.join(self.folder, '01_clean_schema.csv')
        errors=True # JSON_RESPONSE pass the RUBRIC
        max_eval=2
        while errors and counter_fixes<max_eval:
            
            # Generate Response
            pipeline_gen= GenerateResponsePieline()
            pipeline_gen.csv_file_input =fix_file
            clean_file=os.path.join(self.folder,'02_01_response_'+str(counter_fixes)+'.csv')
            pipeline_gen.model=self.model
            pipeline_gen.csv_file_output =  clean_file
            pipeline_gen.process()

            # Eval Code
            pipeline_eval= ValidateResponsePieline()
            pipeline_eval.csv_file_input =clean_file
            eval_code_file=os.path.join(self.folder,'02_02_validate_'+str(counter_fixes)+'.csv')
            pipeline_eval.csv_file_output =  eval_code_file
            pipeline_eval.process()

     

            errors_file=os.path.join(self.folder,'02_03_errors_'+str(counter_fixes)+'.csv')
            fix_file=os.path.join(self.folder,'02_04_fix_file_'+str(counter_fixes)+'.csv')        
            
            # Update the ERROR_CODE to 4 fixed
            if counter_fixes>0:
                #Update pipeline_eval.df['ERROR_CODE'] to 4 when the current value is 0 ok

                pipeline_eval.df.loc[pipeline_eval.df['ERROR_CODE'] == 0, 'ERROR_CODE'] = 4
                #print(pipeline_eval.df['ERROR_CODE'])
            
            # Results
            print(pipeline_eval.df['ERROR_CODE'].value_counts())

            df_ok.append(pipeline_eval.df[pipeline_eval.df['ERROR_CODE']!=2])
            # If the JSON_RESPONSE has errors
            df_errors=pipeline_eval.df[pipeline_eval.df['ERROR_CODE']==2]
            counter_fixes+=1
            if len(df_errors) > 0 and counter_fixes<max_eval:
                
                errors=True
                # Filter the rows with errors

                df_errors.to_csv(errors_file,index=False)

                pipeline_fix= FixPromptPieline()
                pipeline_fix.csv_file_input = errors_file
                pipeline_fix.csv_file_output = fix_file
                pipeline_fix.model=self.model
                pipeline_fix.process()
            else:
                errors=False

            

        # Concat df_ok elements
        # Add last errors to view wrong prompts in the sheet
        df_ok.append(df_errors)
        df_ok=pd.concat(df_ok)
        self.csv_file_output = os.path.join(self.folder,'02_05_eval_response.csv')
        df_ok.to_csv(self.csv_file_output,index=False)


if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python3 pipeline.py <folder> <model>")
        sys.exit(1)
    
    orchestrator=EvalOrchstrator()
    orchestrator.folder=sys.argv[1]
    orchestrator.model=sys.argv[2]
    orchestrator.process()





