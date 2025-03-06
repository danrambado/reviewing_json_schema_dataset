import json
import random
import re
from tara.lib.action import Action

class EvalAction(Action):
    def __init__(self):
        super().__init__()

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
            JSON_SCHEMA = json.loads(row['schema'])
            schema_dict = json.loads(row['schema'])  # Convert string to JSON object
        
            # Extract top-level properties
            properties = schema_dict.get("properties", {})
            extracted_keys = list(properties.keys())  # Extract only top-level keys

            output=[]
            # For each property matched in JSON_MATCH
            for property_name in extracted_keys:
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
Task: Verify Prompt Compliance with JSON Schema

Ensure that the <PROMPT> contains sufficient information to construct a valid JSON based on the provided <JSON_SCHEMA>. 
Every property at all levels of the <JSON_SCHEMA> must be analyzed to determine if it is referenced in the <PROMPT>.

A property is considered referenced if the <PROMPT> explicitly or implicitly includes relevant information that aligns with the schema's structure, the property name and its constraints (data types, allowed values, formats, etc.). 
If a property is not referenced, provide an explanation in the text_reference field.

Reference Types
	•	Explicit: The property or value is directly mentioned in the <PROMPT>.
	•	Implicit: The reference exists through synonyms, descriptions, or context.
	•	Inferred: Logical deduction of a property from the <PROMPT> without direct mention.

Evaluation Criteria
	1.	Property Matching - Does the <PROMPT> reference all properties defined in the <JSON_SCHEMA> (including nested properties at all levels)?
	2.	Value Alignment - If constraints exist (data types, allowed values, formats), does the <PROMPT> provide enough detail to satisfy them? The <PROMPT> doesn't need to follow the exact type described in the schema, as the schema will enforce formatting during JSON generation.
	3.	Completeness & Informational Depth - Does the <PROMPT> capture the full meaning and intent of the <JSON_SCHEMA> without omitting key aspects?

Enhancements to JSON Schema

For each property at all levels of the JSON schema, add the following attributes:
	•	referenced (boolean) - true if the property is referenced in the <PROMPT>, false otherwise.
	•	text_reference (string) - The text from the <PROMPT> that references the property. If no reference exists, provide an explanation.

This must be applied recursively to all nested properties and objects.

Inputs

<PROMPT>
{row['prompt']}
</PROMPT>

<JSON_SCHEMA>
{schema_property}
</JSON_SCHEMA>

Expected Output Format (All Levels Included)

<ANALYSIS>
{{
    "property_a": {{
      "type": "string",
      "referenced": true/false,
      "text_reference": "the text in the prompt that references the property (or an explanation if absent)"
    }},
    "nested_object": {{
      "type": "object",
      "referenced": true/false,
      "text_reference": "..."
      "properties": {{
        "nested_property": {{
          "type": "integer",
          "referenced": true/false,
          "text_reference": "..."
        }},
        "deeply_nested_object": {{
          "type": "object",
          "referenced": true/false,
          "text_reference": "...",
          "properties": {{
            "deepest_property": {{
              "type": "boolean",
              "referenced": true/false,
              "text_reference": "..."
            }}
          }}
        }}
      }}
    }}
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
            output=row['MR_EVAL_SUB_SCHEMA']
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

    def format_json(self, row):
        final_prompt=f"""
Format the <JSON> following the order of the properties in <STRUCTURE>.
Don't change any value of the <JSON>, only the order of the properties.
Just return the formatted JSON.

<JSON>
{row['REFERENCED_JSON']}
<JSON>

<STRUCTURE>
{row['SCHEMA_SIMPLIFIED']}
</STRUCTURE>
        """
        return self.prompt(final_prompt)