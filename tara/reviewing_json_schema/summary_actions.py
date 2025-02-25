from tara.lib.action import Action

class SummaryAction(Action):
    def __init__(self):
        super().__init__()

    def summary(self,row) -> str:
        message=[]
        if str(row['EVAL_SELF_CONTAINED']).lower()=='false':
            message.append('Error Self Contained: '+str(row['EXPLANATION_SELF_CONTAINED']))
        if str(row['EVAL_PII']).lower()=='false':
            message.append('Error PII: '+str(row['EXPLANATION_PII']))
        message.append('Prompt related Score: '+str(row['PROP_SCORE']))
        if row['COUNT_MISSING_PROP']>0:
            message.append(row['JUSTIFICATION_PROP'])
        return '\n'.join(message) if message else ""
    
    def eval(self,row) -> str:
        return (str(row['EVAL_SELF_CONTAINED']).lower()=='true' and str(row['EVAL_PII']).lower()=='true' and row['PROP_SCORE']>0.8)
    
