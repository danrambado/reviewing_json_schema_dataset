from tara.lib.action import Action

class PromptFixer(Action):
    def __init__(self):
        super().__init__()
    
    def prompt_fixer(self,row) -> str:
        final_prompt=f"""
Fix the provided <PROMPT> to ensure that contain the missing reference.
Add the missing refence in a natural way with the existing prompt. Don not add the reference in a forced way or unnaturally. 
Make sure is coherent with the existing prompt.

<MISSING_REFERENCE>
{row['JUSTIFICATION_PROP']}
</MISSING_REFERENCE>

<PROMPT>
{row['prompt']}
</PROMPT>

Your output must follow this structure:
<FIXED_PROMPT>The fixed prompt here</FIXED_PROMPT>
<EXPLANATION>Explanation of the changes</EXPLANATION>
"""
        return self.prompt(final_prompt)