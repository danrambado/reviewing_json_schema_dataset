import random
from tara.lib.action import Action

class EvalPIIAction(Action):
    def __init__(self):
        super().__init__()

    def eval_PII(self,row) -> str:
        prompt=row['prompt']

        final_prompt=f"""
<REQUEST>
Check for personally identifiable information (PII) in the PROMPT.
Fake data are allowed.
Valid examples of false data are contacts such as Anna Fields (anna.fields@email.fake, +15551234567) and Edward Money (edward.money@email.fake).
</REQUEST>

<PROMPT>
    {prompt}
</PROMPT>

Your output must follow this structure:
<PROMPT_OK>True/False</PROMPT_OK>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   
"""
        return self.prompt(final_prompt)
    def promptDummy(self, prompt):
        random_bool = random.choice(['TRUE', 'FALSE'])
        if 'information(PII)' in prompt:
            return f"""
<PROMPT_OK>{random_bool}</PROMPT_OK>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   """
        return super().promptDummy(prompt)
