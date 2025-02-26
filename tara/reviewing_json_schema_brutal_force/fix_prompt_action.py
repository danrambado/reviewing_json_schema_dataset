from tara.lib.action import Action

class FixPromptAction(Action):
    def __init__(self):
        super().__init__()

    def fix_prompt(self,row):
        final_prompt=f"""
    Your response should contain a NEW PROMPT adding the minimum changes to the ORIGINAL_PROMPT to fix this ERROR and continues to align with the JSON_SCHEMA.
    Aggregate changes must refer to property names in natural language without explicitly using the property name.
    
    <ERROR>
    {row['ERROR_MESSAGE']}
    </ERROR>

    <ORIGINAL_PROMPT>
    {row['prompt']}
    </ORIGINAL_PROMPT>

    <JSON_SCHEMA>
    {row['schema']}
    </JSON_SCHEMA>


    Your output must follow this structure:
    <NEW_PROMPT>NEW PROMPT HERE</NEW_PROMPT>
    <EXPLANATION>YOR EXPLANATION HERE<EXPLANATION>
    """
        return self.prompt(final_prompt)
    
    def promptDummy(self, prompt):
        if 'Your response' in prompt:
            return """
    <NEW_PROMPT>NEW PROMPT HERE</NEW_PROMPT>
    <EXPLANATION>YOR EXPLANATION HERE<EXPLANATION>"""
        return super().promptDummy(prompt)