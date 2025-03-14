import random
from tara.lib.action import Action

class EvalPIIAction(Action):
    def __init__(self):
        super().__init__()

    def eval_PII(self,row) -> str:
        ORIGINAL_PROMPT=row['prompt']

        final_prompt=f"""
<REQUEST>
Check if there are full names (first and last name together) in the PROMPT.
</REQUEST>
<PROMPT>
   {{ORIGINAL_PROMPT}}
</PROMPT>

Your output must follow this structure:
<PROMPT_INCLUDE_FULL_NAME>Yes/No</PROMPT_INCLUDE_FULL_NAME>
<EXPLANATION>YOUR SHORT EXPLANATION HERE</EXPLANATION>   
"""
    
        
    def change_prompt(self,row) -> str:
        ORIGINAL_PROMPT=row['FIXED_PROMPT']

        final_prompt=f"""
Make the smallest possible changes to the provided <ORIGINAL_PROMPT> so that full names (first and last name together)
are replaced with the last name and the first initial. Be sure to modify only the full names and not any other text.

<ORIGINAL_PROMPT>
{ORIGINAL_PROMPT}
</ORIGINAL_PROMPT>

Your output must follow this structure:
<FIXED_PROMPT>The fixed prompt here</FIXED_PROMPT>
<EXPLANATION>Explanation of the changes</EXPLANATION>
"""
        return self.prompt(final_prompt)

    def promptDummy(self, prompt):
        random_bool = random.choice(['TRUE', 'FALSE'])
        if 'information(PII)' in prompt:
            return f"""
<PROMPT_OK>{random_bool}</PROMPT_OK>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   """
        return super().promptDummy(prompt)
