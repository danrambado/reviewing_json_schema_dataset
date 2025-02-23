import pandas as pd
import multiprocessing
from rich.console import Console
from rich.progress import track
import sys

class Pipeline:
    def __init__(self):
        self.console = Console()
        self.df = None

    def read_csv(self):
        self.console.log("Reading CSV...")
        self.df = pd.read_csv(self.csv_file_input)
        self.console.log(f"Total number of rows: {len(self.df)}")

    def execute_action(self, action, column):
        # Executes an action in parallel on the DataFrame.
        self.console.log(f"Categorizing {action.__name__} (in parallel)...")
        rows = self.df.to_dict(orient='records')
        with multiprocessing.Pool() as pool:
            values = list(
                    track(
                        pool.imap(action, rows),
                        total=len(self.df),
                        description=f"Processing with {action.__name__}..."
                    )
                )
        self.df[column] = values
    def execute_regex_action(self, regex, column_input, column_output, action):
        action.initialize_regex(regex, column_input)
        self.execute_action(action.regex,column_output)

    def save_csv(self):
        # Saves the DataFrame to a CSV file.
        self.console.log(f"Saving DataFrame to {self.csv_file_output}...")
        self.df.to_csv(self.csv_file_output, index=False)
        self.console.log("Script completed successfully!")

    def process(self):
        # Orchestrates the pipeline by reading the input CSV file, executing the actions in parallel,
        self.console.log("Starting script...")
        self.read_csv()

        
        # Example of how to use the Action class to process the data.
        """
        action = Action()

        action.initialize_default_action("Hello, World!")
        self.execute_action(action.default_action, 'greeting')

        action.set_origin_column_name('PROMPT')
        self.execute_action(action.detect_language, 'from_language')
        
        action.set_origin_column_name('RESPONSE')
        self.execute_action(action.contains_code, 'contains_code')
                
        action.initialize_regex(r"```(.*?)```", 'RESPONSE')
        self.execute_action(action.regex, 'code_snippet')
        """

        # Save the results to a new csv
        self.save_csv()

if __name__ == '__main__':
    orchestrator = Pipeline()
    orchestrator.process()