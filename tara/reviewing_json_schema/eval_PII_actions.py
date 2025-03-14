import random
from tara.lib.action import Action

class EvalPIIAction(Action):
    def __init__(self):
        super().__init__()

    def eval_PII(self,row) -> str:
        ORIGINAL_PROMPT=row['prompt']

        final_prompt=f"""
<REQUEST>
Check for personally identifiable information (PII) in the PROMPT.

We will consider PII as: 
- Full Name (first & last name together)
- Email Address (only if the domain is real)
- Phone Number (only real numbers)
- Home Address (street, city, postal code)
- National ID Number (e.g., Social Security Number, Passport Number, Driver’s License)
- Credit Card Number or Bank Account Number
</REQUEST>

<PROMPT>
   {{ORIGINAL_PROMPT}}
</PROMPT>

Your output must follow this structure:
<PROMPT_INCLUDE_PII>Yes/No</PROMPT_INCLUDE_PII>
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
