from tara.lib.action import Action

class EvalAction(Action):
    def __init__(self):
        super().__init__()

    def eval_match_prompt_json(self,row) -> str:
        final_prompt=f"""
Analyze the provided <PROMPT> and identify any text that references properties defined in <JSON_SCHEMA>.

Generate a JSON output where each key corresponds to a property from <JSON_SCHEMA>, and its value is the relevant text from <PROMPT> that directly or indirectly alludes to that property. 
The reference may be explicit, implicit, or inferred. The key criterion is whether the prompt contains any indication—direct or indirect—of the property's relevance.

If a property is not mentioned in <PROMPT>, assign its value as null. Ensure that all properties from <JSON_SCHEMA> are included in the output JSON.

<PROMPT>
{row['prompt']}
</PROMPT>

<JSON_SCHEMA>
{row['modified_schema']}
</JSON_SCHEMA>

Your output must follow this structure:
<JSON>JSON</JSON>
"""
        return self.prompt(final_prompt)