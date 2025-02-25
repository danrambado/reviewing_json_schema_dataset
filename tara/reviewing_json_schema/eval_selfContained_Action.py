import random
from tara.lib.action import Action

class EvalSelfContainedAction(Action):
    def __init__(self):
        super().__init__()

    def eval_self_containded(self,row) -> str:
        prompt=row['prompt']

        final_prompt=f"""
<REQUEST>
    Your goal is to determine if the given prompt is self-contained, meaning it provides all the necessary context and information to generate a meaningful response without requiring external knowledge.
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
        if 'self-contained' in prompt:
            return f"""
<PROMPT_OK>{random_bool}</PROMPT_OK>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   """
        return super().promptDummy(prompt)
