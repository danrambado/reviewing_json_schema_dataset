from tara.lib.action import Action

class EvalPIIAction(Action):
    def __init__(self):
        super().__init__()

    def eval_PII(self,row) -> str:
        prompt=row['prompt']

        final_prompt=f"""
<REQUEST>
    Check if there is any personal identifiable information(PII) in the PROMPT
</REQUEST>

<PROMPT>
    {prompt}
</PROMPT>

Your output must follow this structure:
<PROMPT_OK>True/False</PROMPT_OK>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   
"""
        return self.prompt(final_prompt)
