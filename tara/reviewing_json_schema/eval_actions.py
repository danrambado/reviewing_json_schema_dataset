import json
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
    

    def eval_sub_schema(self,row) -> str:
        # For each property matched in row['EVAL_PROMPT_MATCH_JSON']
        # Example:
#        {
#               "technique_name": "Convolutional Neural ...",
#               "technique_type": "CNNs are a type of ne...",
#               "architecture": "The core idea behind th...",
#        }

        # Extract the subchema from row['schema']
        # Example:
#{
#    "type": "object",
#    "properties": {
#        "technique_name": {
#            "type": "string"
#        },
#        "technique_type": {
#            "type": "string",
#            "enum": [
#                "Convolutional Neural Network",
#                "Recurrent Neural Network",
#            ]
#        },
#        "architecture": {
#            "type": "object",
#            "properties": {
#                "layers": {
#                    "type": "array",
#                    "items": {
#                        "type": "object",
#                        "properties": {
#                            "layer_type": {
#                                "type": "string"
#                            },
# ...
        
        try:
            JSON_MATCH = json.loads(row['EVAL_PROMPT_MATCH_JSON'])
            JSON_SCHEMA = json.loads(row['schema'])
            output=[]
            # For each property matched in JSON_MATCH
            for property_name, property_value in JSON_MATCH.items():
                if property_value:  # Check if not null
                    # Verify this property exists in the schema
                    if property_name in JSON_SCHEMA.get('properties', {}):
                        # Here we can perform additional validation or processing
                        # for each matched property against its schema definition
                        schema_property = JSON_SCHEMA['properties'][property_name]
                        # Add validation logic as needed
                        
                        output.append('<PROPERTY_NAME>'+property_name+'</PROPERTY_NAME>'+self.call_prompt_sub_schema(row,property_name,schema_property))
        except Exception as e:
            return f"Error {e}"
        return output
        
    def call_prompt_sub_schema(self,row,property_name,schema_property ):
        final_prompt=f"""
Analyze the provided <PROMPT> and identify any text that references properties defined in <JSON_SUB_SCHEMA>.
The <JSON_SUB_SCHEMA> represents the subschema of the property {property_name}, which is a key property in the top-level schema <JSON_SCHEMA>.

Generate a JSON output where each key corresponds to a property from <JSON_SUB_SCHEMA>, and its value is the relevant text from <PROMPT> that directly or indirectly alludes to that property. 
The reference may be explicit, implicit, or inferred. The key criterion is whether the prompt contains any indication—direct or indirect—of the property's relevance.

If a property is not mentioned in <PROMPT>, assign its value as null. Ensure that all properties from <JSON_SUB_SCHEMA> are included in the output JSON.
Evaluate if the prompt include all the information to complete the properties in the <JSON_SUB_SCHEMA>.

<PROMPT>
{row['prompt']}
</PROMPT>

<JSON_SCHEMA>
{row['modified_schema']}
</JSON_SCHEMA>

<JSON_SUB_SCHEMA>
{schema_property}
</JSON_SUB_SCHEMA>

Your output must follow this structure:
<JSON>JSON</JSON>
<PROMPT_OK>True/False</PROMPT_OK>
<EXPLANATION>YOUR EXPLANATION HERE</EXPLANATION>   
"""
        return self.prompt(final_prompt)