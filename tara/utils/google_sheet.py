import os
import sys
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
    
    # download from_sheet_to_csv()
    def from_sheet_to_csv(self, sheet_id, sheet_name, csv_file_name):
        # Open the Google Sheet
        spreadsheet = self.gc.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)

        # Get all values from the worksheet
        data = worksheet.get_all_values()

        # Write to CSV file
        with open(csv_file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: uv run -m tara.utils.google_sheet <sheet> <file>")
        sys.exit(1)

    sheet_id="15SkMV6Frg-4eHuORPAP6Zim9PLxEM5YJzs4bbYZU_c0"
    # Extract the last folder name 
    file_name= sys.argv[1]
    sheet_name= sys.argv[2]
    # Replace Result in Google sheet
    sheet = googleSheet()
    sheet.from_sheet_to_csv(sheet_id, sheet_name, file_name)    