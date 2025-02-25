import json
import random
import re
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
                        schema_property ={property_name: schema_property}
                        # Add validation logic as needed
                        output.append({'property_name':property_name,'analysis':self.call_prompt_sub_schema(row,property_name,schema_property)})
        except Exception as e:
            return f"Error: {e}"
        return output
        
    def call_prompt_sub_schema(self,row,property_name,schema_property ):
        final_prompt=f"""
Analyze the provided subschema and compare it against the PROMPT to determine whether the PROMPT contains references to all relevant aspects of the subschema.
The <JSON_SUB_SCHEMA> represents the subschema of the property {property_name}, which is a key property in the top-level schema <JSON_SCHEMA>.


A reference can be:
	•	Explicit: Directly mentioning a property or value from the subschema.
	•	Implicit: Indirectly alluding to a property through synonyms, descriptions, or contextual information.
	•	Inferred: Logically derived from the content of the PROMPT even if not stated verbatim.

Evaluation Criteria:
	1.	Property Matching: Does the PROMPT reference all required properties in the subschema?
	2.	Value Alignment: If the subschema includes constraints (e.g., types, allowed values, formats), does the PROMPT provide sufficient information to satisfy those constraints?
	3.	Completeness: Does the PROMPT convey enough detail to infer the full meaning of the subschema without missing key aspects?

Expected Output:

Generate a Boolean result (true or false):
	•	true if all elements of the subschema are present, referenced, or inferable from the PROMPT.
	•	false if any element of the subschema is missing or lacks sufficient reference in the PROMPT.

Additionally, provide a justification explaining which properties are fully referenced and which are missing or ambiguous.

Inputs:
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
<ANALYSIS>{{
  "fully_referenced": "true/false",
  "missing_properties": ["prop1", "prop2", ...],  
  "justification": "Explanation of why certain properties are missing or ambiguous."
}}
</ANALYSIS>
"""
        return self.prompt(final_prompt)

    def extract_eval_sub_schema(self,row) -> str:
        # row['MR_EVAL_PROMPT_MATCH_SUB_SCHEMA_JSON]
        try:
            attribute_list=[]
            #print(row['MR_EVAL_PROMPT_MATCH_SUB_SCHEMA_JSON'])
            #output = re.findall(r'<PROPERTY>(.*?)</PROPERTY>', row['MR_EVAL_PROMPT_MATCH_SUB_SCHEMA_JSON'],re.DOTALL)
            output=row['MR_EVAL_PROMPT_MATCH_SUB_SCHEMA_JSON']
            if len(output)==0:
                return []
            for property_ananlysis in output:
                try:
                    #matches_property_name= re.findall(r'<PROPERTY_NAME>(.*?)</PROPERTY_NAME>', match,re.DOTALL)
                    #property_name=matches_property_name[0].strip()
                    matches_analisis= re.findall(r'<ANALYSIS>(.*?)</ANALYSIS>', property_ananlysis['analysis'],re.DOTALL)
                    analysis=matches_analisis[0].strip()
                    json_analysis=json.loads(analysis)
                    json_analysis['property_name']=property_ananlysis['property_name']
                    attribute_list.append(json_analysis)
                except Exception as e:
                    attribute_list.append(f"{{'error':'{e}'}}")
                
            return attribute_list
        except Exception as e:
                return f"'error':'{e}'"
    
    def extract_message(self,row) -> str:
        message=[]
        property_list=row['LIST_JSON_EVAL']
        for property in property_list:
            if ('fully_referenced' in property
             and str(property['fully_referenced']).lower()=='false'):    
                message.append('Error in property "'+property['property_name']+'": '+property['justification'])
        return '\n'.join(message) if message else ""

    

        
        
    def count_prop_fully_referenced(self,row,value=True) -> str:
        json_list=row['LIST_JSON_EVAL']
        count=0
        for eval in json_list:
            if ('fully_referenced' in eval
            and str(eval['fully_referenced']).lower()==str(value).lower()): count+=1
        return count
    
    def count_prop_not_fully_referenced(self,row) -> str:
        return self.count_prop_fully_referenced(row,False)

    def count_missing_prop(self,row) -> str:
        json_list=row['LIST_JSON_EVAL']
        count=0
        for eval in json_list:
            if 'missing_properties' in eval:
                count+=len(eval['missing_properties'])
        return count

    def promptDummy(self, prompt):
        random_bool = random.choice(['TRUE', 'FALSE'])
        if '<JSON_SUB_SCHEMA>' in prompt:
            return f"""
<ANALYSIS>{{
  "fully_referenced": "{random_bool}",
  "missing_properties": ["prop1", "prop2"],  
  "justification": "Explanation of why certain properties are missing or ambiguous."
}}
</ANALYSIS>"""
        elif 'Analyze the provided <PROMPT>' in prompt:
            return """
<JSON>
{
       "technique_name": "Convolutional Neural ...",
       "technique_type": "CNNs are a type of ne...",
       "architecture": "The core idea behind th..."
}
</JSON>"""
        return super().promptDummy(prompt)


if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    row={}
    row['MR_EVAL_PROMPT_MATCH_SUB_SCHEMA_JSON']=[{'property_name':'XX',
                                                  'analysis':"""
'<ANALYSIS>{
  "fully_referenced": "true/false",
  "missing_properties": ["prop1", "prop2"],  
  "justification": "Explanation of why certain properties are missing or ambiguous."
}
</ANALYSIS>
'"""}
,{'property_name':'YY',
'analysis':"""
'<ANALYSIS>{
  "fully_referenced": "true/false",
  "missing_properties": ["prop1", "prop2"],  
  "justification": "Explanation of why certain properties are missing or ambiguous."
}
</ANALYSIS>
'"""}]
    action=EvalAction()
    print(action.extract_eval_sub_schema(row))
