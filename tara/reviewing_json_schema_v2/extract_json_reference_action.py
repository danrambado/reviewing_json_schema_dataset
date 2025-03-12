import json
from tara.lib.action import Action

import pandas as pd
import ast



class ExtractJsonReferenceAction(Action):
    def __init__(self):
        super().__init__()

    # Function to count the number of properties in True and the number of properties in False of JSON
    # json example
    #[
    #    {
    #        "act_summaries": {
    #            "type": "array",
    #            "referenced": true,
    #            "text_reference": "The prompt includes an 'Act Summaries' section with multiple acts (Act 1, Act 2, etc.) describing their content.",
    #            "items": {
    #                "type": "object",
    #                "properties": {
    #                    "act_number": {
    #                        "type": "integer",
    #                        "referenced": true,
    #                        "text_reference": "Each act is identified by its number in phrases like 'Act 1:', 'Act 2:', etc., which implies a numerical identifier."
    #                    },
    #                    "summary": {
    #                        "type": "string",
    #                        "referenced": true,
    #                        "text_reference": "For every act, a narrative description is provided (e.g., 'The play opens with guards encountering the ghost of King Hamlet' for Act 1) summarizing the act."
    #                    },
    #                    "scene_summaries": {
    #                        "type": "array",
    #                        "referenced": true,
    #                        "text_reference": "The prompt includes detailed 'Scene Summaries' for selected acts (e.g., Act 1, Scene 1; Act 1, Scene 5; Act 3, Scene 2; Act 5, Scene 1; Act 5, Scene 2).",
    #                        "items": {
    #                            "type": "object",
    #                            "properties": {
    #                                "scene_number": {
    #                                    "type": "integer",
    #                                    "referenced": true,
    #                                    "text_reference": "Each scene is identified by a number in the text such as 'Scene 1' or 'Scene 2' attached to its act (e.g., 'Act 1, Scene 1')."
    #                                },
    #                                "setting": {
    #                                    "type": "string",
    #                                    "referenced": true,
    #                                    "text_reference": "Settings for scenes are explicitly described (e.g., 'Elsinore', 'The battlements', 'A hall in the castle', 'A churchyard')."
    #                                },
    #                            }
    #                        }
    #                    }
    #                },
    #                "required": [
    #                    "act_number",
    #                    "summary"
    #                ]
    #            }
    #        },
    #        "property_name": "act_summaries"
    #    },
    #
    #]
    def count_referenced_properties(json_data):
        true_count = 0
        false_count = 0
        referenced_true = []
        referenced_false = []

        def count_references(obj, parent_key=''):
            nonlocal true_count, false_count
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'referenced':
                        if value:
                            true_count += 1
                            referenced_true.append(parent_key)
                        else:
                            false_count += 1
                            referenced_false.append(parent_key)
                    else:
                        count_references(value, key if parent_key == '' else f"{parent_key}.{key}")
            elif isinstance(obj, list):
                for item in obj:
                    count_references(item, parent_key)

        count_references(json_data)
        return true_count, false_count, ExtractJsonReferenceAction.remove_properties_suffix(referenced_true), ExtractJsonReferenceAction.remove_properties_suffix(referenced_false)

    # function to count the number of properties of the json schema
    def count_properties_schema(json_schema):
        property_names = []

        def count_props(obj, parent_key=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'properties':
                        property_names.extend([f"{parent_key}.{k}" if parent_key else k for k in value.keys()])
                    count_props(value, key if parent_key == '' else f"{parent_key}.{key}")
            elif isinstance(obj, list):
                for item in obj:
                    count_props(item, parent_key)

        count_props(json_schema)
        return ExtractJsonReferenceAction.remove_properties_suffix(property_names)

    def remove_properties_suffix(strings):
        return [s.replace('properties.', '').replace('if.','').replace('then.','').replace('else.','').replace('oneOf.','').replace('allOf.','').replace('anyOf.','') for s in strings]

    # Clean adn load json
    def extract_json(referenced_json):
        
        #referenced_json = ast.literal_eval(referenced_json)

        #referenced_json = json.loads(json.dumps(referenced_json))
        #Uncomment this line to read from csv
        return referenced_json
        return json.dumps(referenced_json, indent=4)
        # For long schemas
        #return json.dumps(referenced_json)

    def summary(json_schema,referenced_json):
    # Example usage with the provided JSON schema
        property_count = ExtractJsonReferenceAction.count_properties_schema(json_schema)

        true_count, false_count, referenced_true, referenced_false = ExtractJsonReferenceAction.count_referenced_properties(referenced_json)

        # Find the difference between property_count and referenced_true
        difference = list(set(property_count) - set(referenced_true))
        match=len(property_count)-len(difference)

        #create a list of intersect of referenced_false and property_count
        referenced_false = list(set(referenced_false) & set(property_count))

        difference_missing = list(set(difference) - set(referenced_false))

        coditional_sentence = '"if":' in json.dumps(json_schema)

        accuracy = 1-len(difference_missing)/len(property_count)

        return {"schema_count": len(property_count),
                "referenced_true": match,
                "score_reference": match/len(property_count),
                "list_missing_properties_prompt": difference_missing,
                "missing_properties_prompt": len(difference_missing),
                "list_referenced_false": referenced_false,
                "referenced_false": len(referenced_false),
                "coditional_sentence": coditional_sentence,
                "accuracy": accuracy
            }

    #function to format the json in this output string 
    #Number of Properties in the Schema:
    #Properties mentioned in the prompt (according to the LLM):
    #    •   Count:
    #Properties not mentioned in the prompt (according to the LLM):
    #    •   Count:
    #    •   List:
    #Properties not evaluated by the model:
    #    •   Count:
    #    •   List: (edited)
    def format_summary_output(summary_dict):
        output = (
            f"Number of Properties in the Schema: {summary_dict['schema_count']}\n"
            f"Properties mentioned in the prompt (according to the LLM):\n"
            f"    •   Count: {summary_dict['referenced_true']}\n"
            f"Properties not mentioned in the prompt (according to the LLM):\n"
            f"    •   Count: {summary_dict['referenced_false']}\n"
            f"    •   List: {', '.join(summary_dict['list_referenced_false'])}\n"
            f"Properties not evaluated by the model:\n"
            f"    •   Count: {summary_dict['missing_properties_prompt']}\n"
            f"    •   List: {', '.join(summary_dict['list_missing_properties_prompt'])}\n"        
        )
        if summary_dict['coditional_sentence']:
            output+= "\nNote: The schema includes conditional sentences."
        return output
    
    def extract_referenced_json(self,row):
        return ExtractJsonReferenceAction.extract_json(row['REFERENCED_JSON'])
    
    def summary_json(self,row):
        try:
            return ExtractJsonReferenceAction.summary(json.loads(row['schema']), json.loads(row['REFERENCED_JSON_FORMATED']))
        except Exception as e:
            return {"error": str(e)}
    
    def summary_format(self,row):
        try:
            return ExtractJsonReferenceAction.format_summary_output(row['summary_json'])
        except Exception as e:
            return {"error": str(e)}
