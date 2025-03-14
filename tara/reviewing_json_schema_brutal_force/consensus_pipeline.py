import sys
import pandas as pd
from difflib import SequenceMatcher
class ConsensusPipeline():
    def __init__(self):
        pass
        
    def process(self):
        df1=pd.read_csv(self.file1)
        df2=pd.read_csv(self.file2)
        # Create a new df df1 join df2 by TASK_ID with the columns:
        # values of df1: LAST_ATTEMPTER_NAME	LAST_ATTEMPTER_EMAIL	FIRST_ATTEMPTER_NAME	FIRST_ATTEMPTER_EMAIL	ATTEMPT_COUNT	ATTEMPTERS_LIST_MAIL	REVIEW_LEVEL	STATUS	ATTEMPTED_AT	ATTEMPTED_AT_DATE	TASK_ID	ATTEMPT_ID	REVIEW_STATUS	prompt	schema	OTHER_PROMPT_ISSUES	OTHER_PROMPT_ISSUES_JUST	PROMPT_PII	PROMPT_PII_JUST	SCHEMA_RELATED	SCHEMA_RELATED_JUST	SUFFICIENT_INFORMATION	SUFFICIENT_INFORMATION_JUST	COMPLEX_FIXING	FIXED_PROMPT	CH_PROMPT	QC Score	Feedback
        # rename the column in df1 by adding prefix "01_": MR_JSON_RESPONSE	JSON_RESPONSE	MR_VALIDATE_RESPONSE	VALIDATE_RESPONSE	ERROR_MESSAGE	ERROR_CODE	MR_FIX_PROMPT	NEW_PROMPT	EXPLANATION_FIXED_PROMPT	HISTORY_MR_VALIDATE_RESPONSE	HISTORY_JSON_RESPONSE
        # rename the column in df2 by adding prefix "01_": MR_JSON_RESPONSE	JSON_RESPONSE	MR_VALIDATE_RESPONSE	VALIDATE_RESPONSE	ERROR_MESSAGE	ERROR_CODE	MR_FIX_PROMPT	NEW_PROMPT	EXPLANATION_FIXED_PROMPT	HISTORY_MR_VALIDATE_RESPONSE	HISTORY_JSON_RESPONSE
        # Columns to keep from df1 without renaming
        keep_cols = ['LAST_ATTEMPTER_NAME', 'LAST_ATTEMPTER_EMAIL', 'FIRST_ATTEMPTER_NAME', 
                     'FIRST_ATTEMPTER_EMAIL', 'ATTEMPT_COUNT', 'ATTEMPTERS_LIST_MAIL', 
                     'REVIEW_LEVEL', 'STATUS', 'ATTEMPTED_AT', 'ATTEMPTED_AT_DATE', 
                     'TASK_ID', 'ATTEMPT_ID', 'REVIEW_STATUS', 'prompt', 'schema',
                     'OTHER_PROMPT_ISSUES', 'OTHER_PROMPT_ISSUES_JUST', 'PROMPT_PII',
                     'PROMPT_PII_JUST', 'SCHEMA_RELATED', 'SCHEMA_RELATED_JUST',
                     'SUFFICIENT_INFORMATION', 'SUFFICIENT_INFORMATION_JUST',
                     'COMPLEX_FIXING', 'FIXED_PROMPT', 'CH_PROMPT', 'QC Score', 'Feedback']
        keep_cols = ['languageCode','internal_id','prompt','schema']
        # Columns to rename with prefix
        rename_cols = ['MR_JSON_RESPONSE', 'JSON_RESPONSE', 'MR_VALIDATE_RESPONSE',
                      'VALIDATE_RESPONSE', 'ERROR_MESSAGE', 'ERROR_CODE', 'MR_FIX_PROMPT',
                      'NEW_PROMPT', 'EXPLANATION_FIXED_PROMPT', 'HISTORY_MR_VALIDATE_RESPONSE',
                      'HISTORY_JSON_RESPONSE']

        # Rename columns in both dataframes
        for col in rename_cols:
            if col in df1.columns:
                df1 = df1.rename(columns={col: f"01_{col}"})
            if col in df2.columns:
                df2 = df2.rename(columns={col: f"02_{col}"})
        column_join='TASK_ID'
        column_join='internal_id'

        # Merge dataframes
        merged_df = pd.merge(df1[keep_cols + [f"01_{col}" for col in rename_cols if f"01_{col}" in df1.columns]], 
                            df2[[f"02_{col}" for col in rename_cols if f"02_{col}" in df2.columns] + [column_join]], 
                            on=column_join)
        # Consensus 1 both ERROR_CODE=0
        merged_df['CONSENSUS'] = (merged_df['01_ERROR_CODE'] == 0) & (merged_df['02_ERROR_CODE'] == 0)

        # Consensus 2 if ERROR_CODE in (2,4) and similarity of HISTORY_MR_VALIDATE_RESPONSE
        # Check if ERROR_CODE is in (2,4) for both reviewers
        error_code_match = (merged_df['01_ERROR_CODE'].isin([2,4])) & (merged_df['02_ERROR_CODE'].isin([2,4]))

        # Check if HISTORY_MR_VALIDATE_RESPONSE is similar (60% threshold)
        def similar(a, b, threshold=0.6):
            return SequenceMatcher(None, str(a), str(b)).ratio() >= threshold
        
        history_match = merged_df.apply(lambda x: similar(x['01_HISTORY_MR_VALIDATE_RESPONSE'], 
                                x['02_HISTORY_MR_VALIDATE_RESPONSE']), axis=1)

        # Update CONSENSUS where both conditions are met
        merged_df.loc[error_code_match & history_match, 'CONSENSUS'] = True

        print(merged_df[['01_ERROR_CODE','02_ERROR_CODE','CONSENSUS']])

        merged_df.to_csv(self.output)   

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 pipeline.py <file1> <file2> <output>")
        sys.exit(1)
    
    orchestrator=ConsensusPipeline()
    orchestrator.file1=sys.argv[1]
    orchestrator.file2=sys.argv[2]
    orchestrator.output=sys.argv[3]
    orchestrator.process()