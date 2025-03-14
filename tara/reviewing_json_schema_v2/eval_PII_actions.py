import random
from tara.lib.action import Action

class EvalPIIAction(Action):
    def __init__(self):
        super().__init__()

    def eval_PII(self,row) -> str:
        ORIGINAL_PROMPT=row[self.origin_colum_name]
        if ORIGINAL_PROMPT==None:
            return """<PROMPT_INCLUDE_PII>No</PROMPT_INCLUDE_PII>
<EXPLANATION>Not Found</EXPLANATION>"""
        final_prompt=f"""
<REQUEST>
Check for personally identifiable information (PII) in the PROMPT.

We will consider PII as: 
- Email Address (only if the domain is real)
- Phone Number (only real numbers)
- Home Address (street, city, postal code)
- National ID Number (e.g., Social Security Number, Passport Number, Driver’s License)
- Credit Card Number or Bank Account Number
</REQUEST>

<PROMPT>
   {ORIGINAL_PROMPT}
</PROMPT>

Your output must follow this structure:
<PROMPT_INCLUDE_PII>Yes/No</PROMPT_INCLUDE_PII>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   
"""
        return self.prompt(final_prompt)
    
    def eval_full_names(self,row) -> str:
        ORIGINAL_PROMPT=row[self.origin_colum_name]
        if ORIGINAL_PROMPT==None:
            return """<PROMPT_INCLUDE_FULL_NAMES>No</PROMPT_INCLUDE_FULL_NAMES>
<EXPLANATION>Not Found</EXPLANATION>"""
        final_prompt=f"""
<REQUEST>
Check if there are full names (first and last name together) in the PROMPT.
</REQUEST>
<PROMPT>
   {ORIGINAL_PROMPT}
</PROMPT>
Your output must follow this structure:
<PROMPT_INCLUDE_FULL_NAMES>Yes/No</PROMPT_INCLUDE_FULL_NAMES>
<EXPLANATION>YOUR SHORT EXPLANATION HERE</EXPLANATION>
"""
        return self.prompt(final_prompt)

    def eval_company_names(self,row) -> str:
        ORIGINAL_PROMPT=row[self.origin_colum_name]
        if ORIGINAL_PROMPT==None:
            return """<PROMPT_INCLUDE_COMPANY_NAMES>No</PROMPT_INCLUDE_COMPANY_NAMES>
<EXPLANATION>Not Found</EXPLANATION>"""
        final_prompt=f"""
<REQUEST>
Check if the PROMPT INCLUDES REAL mid-sized/chic companies that are not known worldwide.  For example; “InnovateTech Solutions” is a company that may exist so it should be flagged as "Yes" the prompt include company names.
</REQUEST>

<PROMPT>
   {ORIGINAL_PROMPT}
</PROMPT>

Your output must follow this structure:
<PROMPT_INCLUDE_COMPANY_NAMES>Yes/No</PROMPT_INCLUDE_COMPANY_NAMES>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   """
        return self.prompt(final_prompt)

    def eval_original_prompt(self,row):
        result = row['EVAL_FULL_NAMES'].lower()=='yes' or row['EVAL_PII'].lower()=='yes' or row['EVAL_COMPANY_NAMES'].lower()=='yes'
        return 'Yes' if result else 'No'
    
    def eval_fixed_prompt(self,row):
        result= row['EVAL_FULL_NAMES_FIXED'].lower()=='yes' or row['EVAL_PII_FIXED'].lower()=='yes' or row['EVAL_COMPANY_NAMES_FIXED'].lower()=='yes'
        return 'Yes' if result else 'No'

    def promptDummy(self, prompt):
        random_bool = random.choice(['TRUE', 'FALSE'])
        if 'information(PII)' in prompt:
            return f"""
<PROMPT_OK>{random_bool}</PROMPT_OK>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   """
        return super().promptDummy(prompt)
