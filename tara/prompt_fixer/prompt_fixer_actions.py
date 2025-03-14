from tara.lib.action import Action

class PromptFixer(Action):
    def __init__(self):
        super().__init__()
    
    def prompt_fixer(self,row) -> str:
        final_prompt=f"""

Fix the provided  <ORIGINAL_PROMPT> by making the smallest possible changes to include a MISSING_REFERENCE.
Additionally:
- The changes should be minimal—only adding what's necessary.
- The new reference should fit smoothly without making the prompt sound unnatural.
- When describing changes, refer to property names in natural language instead of explicitly mentioning them.

<MISSING_REFERENCE>
{row['JUSTIFICATION_PROP']}
</MISSING_REFERENCE>

<ORIGINAL_PROMPT>
{row['prompt']}
</ORIGINAL_PROMPT>

Your output must follow this structure:
<FIXED_PROMPT>The fixed prompt here</FIXED_PROMPT>
<EXPLANATION>Explanation of the changes</EXPLANATION>
"""
        return self.prompt(final_prompt)