import gspread
import csv
from gspread.exceptions import WorksheetNotFound

class googleSheet:
    def __init__(self):
        # 1. **Authorize access to Google Sheets**
        #   - You'll need to set up a project in the Google Cloud Console and enable the Google Sheets API.
        #   - Download the credentials JSON file and save it as 'credentials.json'.

        self.gc = gspread.service_account(filename='googleSheetCredentials.json')

    def from_csv_to_sheet(self, csv_file_name, sheet_id, sheet_name, mode='replace'):
        # 2. **Open the Google Sheet**
        spreadsheet = self.gc.open_by_key(sheet_id)

        # 3. **Check if the worksheet exists, otherwise create it.**
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except WorksheetNotFound:
            # Create a new worksheet with default size (100 rows, 20 columns)
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)

        # 4. **Open the local CSV file**
        with open(csv_file_name, 'r') as file_obj:
            reader = csv.reader(file_obj)
            data = list(reader)

        # 5. **Write the data to the Google Sheet**
        if mode == 'append':
            # Append the data (excluding the header if you only want to append rows)
            worksheet.append_rows(data[1:])
        elif mode == 'replace':
            worksheet.clear()
            worksheet.update('A1', data)