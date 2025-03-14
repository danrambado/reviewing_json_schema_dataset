from tara.lib.action import Action
import json

class EvalActionv2(Action):
    def __init__(self):
        super().__init__()

    def eval_match_prompt_json(self,row) -> str:
        final_prompt=f"""
Analyze the provided <JSON_SCHEMA> and compare it against the PROMPT to determine whether the PROMPT contains references to all relevant aspects of the <JSON_SCHEMA>.
Generate a new JSON where each key corresponds to a property in <JSON_SCHEMA>, and the value is the relevant text from <PROMPT> that alludes to that property. 
If a required property is not mentioned in <PROMPT>, its value should be null.

A reference can be:
	•	Explicit: Directly mentioning a property or value from the <JSON_SCHEMA>.
	•	Implicit: Indirectly alluding to a property through synonyms, descriptions, or contextual information.
	•	Inferred: Logically derived from the content of the PROMPT even if not stated verbatim.

Evaluation Criteria:
	1.	Property Matching: Does the PROMPT reference all required properties in the <JSON_SCHEMA>?
	2.	Value Alignment: If the <JSON_SCHEMA> includes constraints (e.g., types, allowed values, formats), does the PROMPT provide sufficient information to satisfy those constraints?
	3.	Completeness: Does the PROMPT convey enough detail to infer the full meaning of the <JSON_SCHEMA> without missing key aspects?
  4.  Extra Properies: Does the PROMPT reference additional properties/values not included in the <JSON_SCHEMA>?

Expected Output:

Generate a Boolean result (true or false):
	•	true if all elements of the <JSON_SCHEMA> are present, referenced, or inferable from the PROMPT and the PROMPT does not include additional elements not included in the <JSON_SCHEMA>.
	•	false if any element of the <JSON_SCHEMA> is missing or lacks sufficient reference in the PROMPT or the PROMPT includes additional elements not included in the <JSON_SCHEMA>.

Additionally, provide a justification explaining which properties are fully referenced and which are missing or ambiguous.

Inputs:
<PROMPT>
{row['prompt']}
</PROMPT>

<JSON_SCHEMA>
{row['schema']}
</JSON_SCHEMA>

Your output must follow this structure:
<JSON>HERE NEW JSON</JSON>
<ANALYSIS>{{
  "fully_referenced": "true/false",
  "extra_properties": ["prop1", "prop2", ...],
  "justification": "Explanation of why certain properties are missing, ambiguous or extra."
}}
</ANALYSIS>
"""
        return self.prompt(final_prompt)
    
    def count_properties_json(self,json,OK=True):
        
            # search all the properties in the json
            properties = []
            def search_properties(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if ((value!=None)==OK):
                            properties.append(key)
                        search_properties(value)
                elif isinstance(obj, list):
                    for item in obj:
                        search_properties(item)

            search_properties(json)
            return len(properties)


    def count_match_properties(self,row):
        # create JSON_var from row['EVAL_PROMPT_MATCH_JSON']
        try:
            JSON_var = json.loads(row['EVAL_PROMPT_MATCH_JSON'])
            return self.count_properties_json(JSON_var,True)
        except json.JSONDecodeError:
            return 0

    def count_missing_prop(self,row):
        # create JSON_var from row['EVAL_PROMPT_MATCH_JSON']
        try:
            JSON_var = json.loads(row['EVAL_PROMPT_MATCH_JSON'])
            return self.count_properties_json(JSON_var,False)
        except json.JSONDecodeError:
            return 0

    def count_prop_fully_referenced(self,row,OK=True):
        # create JSON_var from row['EVAL_PROMPT_MATCH_JSON']
        fully_referenced=0
        try:
            obj = json.loads(row['EVAL_PROMPT_MATCH_JSON'])
            # search all the properties in the json
            if isinstance(obj, dict) and len(obj.items())==1 :
                #assing obj to the first item in obj
                key, obj = list(obj.items())[0]
                
            if isinstance(obj, dict):
                for key, value in obj.items():
                    error=False
                    if value!=None:
                        if self.count_properties_json(value,False)>0:
                            error=True
                    else:
                        error=True

                    if (error!=OK):
                        fully_referenced+=1
            elif isinstance(obj, list):
                for item in obj:
                    error=False
                    if item!=None:
                        if self.count_properties_json(item,False)>0:
                            error=True
                    else:
                            error=True
                    if (error!=OK):
                        fully_referenced+=1                        

            return fully_referenced
        except json.JSONDecodeError:
            return 0

    def count_prop_not_fully_referenced(self,row):
        return self.count_prop_fully_referenced(row,False)

    def extract_message(self,row):
        try:
            obj = json.loads(row['LIST_JSON_EVAL'])
            if 'justification' in obj:
                return obj['justification']
            else: return ''
        except Exception as e:
            return str(e)

    def count_extra_properties(self,row):
        try:
            obj = json.loads(row['LIST_JSON_EVAL'])
            if 'extra_properties' in obj:
                return len(obj['extra_properties'])
            else: return 0
        except Exception as e:
            return 0

    def promptDummy(self, prompt):
        if '<JSON_SCHEMA>' in prompt:
            return '''
<JSON>
{
  "technique_name": "Convolutional Neural Networks (CNNs)",
  "technique_type": "Convolutional Neural Network",
  "architecture": {
    "layers": [
      {
        "layer_type": "Convolutional layers"
      },
      {
        "layer_type": "Pooling layers"
      },
      {
        "layer_type": "Fully Connected layers"
      }
    ],
    "activation_functions": ["ReLU", "Sigmoid", "Tanh", "Softmax"],
    "pooling_layers": ["Max Pooling", "Average Pooling"],
    "recurrent_units": null,
    "attention_mechanism": null,
    "embedding_dimension": null,
    "number_of_heads": null,
    "feedforward_dimension": null
  },
  "training_process": {
    "optimizer": ["Adam", "SGD", "RMSprop"],
    "loss_function": ["CrossEntropyLoss", "MSELoss"],
    "regularization": {
      "l1_regularization": null,
      "l2_regularization": null,
      "dropout_rate": null,
      "batch_normalization": true,
      "layer_normalization": null
    },
    "data_augmentation": ["rotation", "flipping", "cropping", "noise_injection"],
    "batch_size": "Typically ranges from 32 to 256",
    "epochs": "Depends on the dataset and network complexity",
    "learning_rate": "Adaptive learning rate",
    "learning_rate_scheduler": ["StepLR", "ExponentialLR", "ReduceLROnPlateau"]
  }
}
</JSON>
<ANALYSIS>
{
  "fully_referenced": "true",
  "missing_properties": ["prop1", "prop2"],
  "extra_properties": ["prop1", "prop2"],
  "justification": "Explanation of why certain properties are missing, ambiguous or extra."
}
</ANALYSIS>
'''
        return super().promptDummy(prompt)
    
if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    row={}
    row['EVAL_PROMPT_MATCH_JSON']="""{
  "businessSupportInitiatives": [
    {
      "initiativeName": "London Startup Seed Fund",
      "initiativeDescription": "An initiative designed to provide crucial early-stage financial support and mentorship to innovative tech startups within London.",
      "supportType": ["Financial Assistance", "Mentorship"],
      "targetAudience": ["Startup", "Early-Stage"],
      "eligibilityCriteria": {
        "businessType": ["Technology"],
        "businessSize": {
          "employeeCount": {
            "minimum": 1,
            "maximum": 10
          },
          "annualRevenue": {
            "minimum": null,
            "maximum": 500000,
            "currency": "GBP"
          }
        },
        "location": ["London"],
        "industrySector": ["Tech"],
        "operationalStage": ["Startup", "Early-Stage"],
        "additionalCriteria": null,
        "specificDemographics": null
      },
      "applicationProcess": {
        "applicationMethod": ["Online Portal"],
        "applicationDocumentsRequired": ["Detailed business plan", "Comprehensive financial projections"],
        "applicationDeadline": "2024-12-31",
        "reviewProcessDescription": "Funds are disbursed quarterly after a successful review process conducted by a panel of innovation experts.",
        "contactInformation": {
          "department": "Startup Support Department",
          "email": "support@londonstartupseedfund.uk",
          "phone": "020-1234-5678"
        }
      },
      "fundingDetails": {
        "fundingAmount": {
          "minimumAmount": 10000,
          "maximumAmount": 50000,
          "currency": "GBP"
        },
        "fundingType": "Grant",
        "disbursementSchedule": "Quarterly after successful review process",
        "matchingRequirement": "No matching fund requirements"
      },
      "programMetrics": {
        "successMetrics": ["Job creation", "Revenue growth"],
        "reportingRequirements": "Reporting is required annually.",
        "impactMeasurementMethodology": "Assessed based on the startup's contribution to London's tech ecosystem."
      },
      "sponsoringOrganizations": ["Innovate UK"],
      "geographicScope": ["London"],
      "initiativeStatus": "Active",
      "termsAndConditions": "Please refer to the program website.",
      "relatedResources": ["Online workshop series for startups"],
      "applicationLink": "Provided on Innovate UK’s website under the ‘Startup Support’ section."
    },
    {
      "initiativeName": "SME Growth Catalyst Program",
      "initiativeDescription": "Aimed at supporting the expansion of established Small and Medium-sized Enterprises (SMEs) in London.",
      "supportType": ["Training and Development", "Networking"],
      "targetAudience": ["Growth-Stage", "Mature"],
      "eligibilityCriteria": {
        "businessType": ["SME"],
        "businessSize": {
          "employeeCount": {
            "minimum": 50,
            "maximum": 250
          },
          "annualRevenue": {
            "minimum": 1000000,
            "maximum": 25000000,
            "currency": "GBP"
          }
        },
        "location": ["London"],
        "industrySector": ["All industry sectors"],
        "operationalStage": ["Growth-Stage", "Mature"],
        "additionalCriteria": null,
        "specificDemographics": null
      },
      "applicationProcess": {
        "applicationMethod": ["Email Submission"],
        "applicationDocumentsRequired": ["Company registration document", "Last year's financial statement"],
        "applicationDeadline": "2024-11-30",
        "reviewProcessDescription": "Applications are reviewed by the SME Growth Committee.",
        "contactInformation": {
          "department": "SME Growth Team",
          "email": "info@smegrowthcatalyst.uk",
          "phone": "020-9876-5432"
        }
      },
      "fundingDetails": {
        "fundingAmount": null,
        "fundingType": null,
        "disbursementSchedule": null,
        "matchingRequirement": "No direct funding associated."
      },
      "programMetrics": {
        "successMetrics": ["Business expansion", "Market share increase"],
        "reportingRequirements": "Reporting is bi-annual.",
        "impactMeasurementMethodology": "Evaluated based on the program's contribution to SME sector growth in London."
      },
      "sponsoringOrganizations": ["Department for Business and Trade, UK"],
      "geographicScope": ["London"],
      "initiativeStatus": "Ongoing",
      "termsAndConditions": "Standard SME support terms and conditions apply.",
      "relatedResources": ["Access to industry-specific reports", "Market analysis"],
      "applicationLink": "Apply@smegrowthcatalyst.uk"
    }
  ]
}
"""
    action=EvalActionv2()
    print('match properties:',action.count_match_properties(row))
    print('Not match properties:',action.count_missing_prop(row))

    print('First level fully referenced:',action.count_prop_fully_referenced(row))
    print('First level not fully referenced',action.count_prop_not_fully_referenced(row))

