import re
from tara.lib.action import Action

class GenerateResponseAction(Action):
    def __init__(self):
        super().__init__()

    def generate_response(self,row):
        if 'NEW_PROMPT' in row:
            prompt=row['NEW_PROMPT']
        else:
            prompt=row['prompt']
        final_prompt=f"""
    Your response must contain a valid JSON and conform to the provided JSON_SCHEMA and PROMPT:

    <PROMPT>
    {prompt}
    </PROMPT>

    <JSON_SCHEMA>
    {row['schema']}
    </JSON_SCHEMA>

    Your output must follow this structure:
    <JSON_RESPONSE>HERE YOUR JSON RESPONSE</JSON_RESPONSE>
    """
        return self.prompt(final_prompt)
    
    def extract_json(self,row):
        output = re.findall(r"<JSON_RESPONSE>(.*?)</JSON_RESPONSE>", str(row['MR_JSON_RESPONSE']),re.DOTALL)
        
        if len(output)!=1:
            output = re.findall(r'```json\n(.*?)```', str(row['MR_JSON_RESPONSE']),re.DOTALL)
            if len(output)==1:
                return output[0]
            else:
                return ''
        else:
            return output[0]

    def promptDummy(self, prompt):
        if 'Your response' in prompt:
            return """
{'a':'text'}"""
        return super().promptDummy(prompt)
    
if __name__ == '__main__':
    row={}
    row['MR_JSON_RESPONSE']="""
<JSON_RESP
```json
cod
dododo
``
</JSON_RESPONSE>"""
    action=GenerateResponseAction()
    print(action.extract_json(row))