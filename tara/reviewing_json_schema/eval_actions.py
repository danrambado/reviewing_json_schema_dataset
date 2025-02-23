from tara.lib.action import Action

class EvalAction(Action):
    def __init__(self):
        super().__init__()

    def eval_match_prompt_json(self,row) -> str:
        final_prompt=f"""
Analyze the given <PROMPT> and extract any text that references properties defined in <JSON_SCHEMA>. 
Generate a new JSON where each key corresponds to a property in <JSON_SCHEMA>, and the value is the relevant text from <PROMPT> that alludes to that property. 
If a property is not mentioned in <PROMPT>, its value should be null. Ensure all properties from <JSON_SCHEMA> are included in the output.

<PROMPT>
{row['prompt']}
</PROMPT>

<JSON_SCHEMA>
{row['schema']}
</JSON_SCHEMA>

Your output must follow this structure:
<JSON>JSON</JSON>
"""
        return self.prompt(final_prompt)