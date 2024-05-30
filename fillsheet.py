""" You must run 'pip install -r requirements.txt' before running this script."""
from datetime import datetime
import locale
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
import gspread

driver = webdriver.Chrome()

driver.get("Your file")

driver.execute_script("updateTotals()")
success_percentage = driver.find_element("id", "scs").text
version = "your version"
success_percentage = int(float(success_percentage.split("(")[1].split("%")[0]))

print(success_percentage)

driver.quit()

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

KEY_FILE = "quiet-cider.json"

creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, scope)

client = gspread.authorize(creds)

spreadsheet = client.open_by_url("file")

worksheet = spreadsheet.get_worksheet(3)
locale.setlocale(locale.LC_TIME, "pt_BR.utf8") #Current set to Brazilian Portuguese locale
current_date = datetime.now().strftime("%d-%b").lower()

FIRST_START_ROW = 34
FIRST_END_ROW = 141
SECOND_SYART_ROW = 142
SECOND_END_ROW = 217


def fetch_rows(start_row, end_row):
    """
    Fetches rows from a worksheet based on the specified start and end row numbers.

    Args:
        start_row (int): The starting row number.
        end_row (int): The ending row number.

    Returns:
        None

    Prints the status of each row, indicating whether it is empty or filled, along with its contents.
    If an empty row is encountered, the function keeps track of the first empty row encountered.

    """
    first_empty_row = None

    all_values = worksheet.get_all_values()
    rows = all_values[start_row-1:end_row]
    for i, row in enumerate(rows, start=start_row):
        if not row or all(cell == '' for cell in row):
            print(f"Row {i} is empty.")
            if first_empty_row is None:
                first_empty_row = i
        else:
            print(f"Row {i} is filled. Contents: {row}")


def insert_content_matching_date(start_row, end_row, date_to_match):
    """
    Inserts content into the worksheet based on a given date.

    Args:
        start_row (int): The starting row index.
        end_row (int): The ending row index.
        date_to_match (str): The date to match.

    Returns:
        bool: True if content is inserted, False otherwise.
    """
    all_values = worksheet.get_all_values()
    rows = all_values[start_row-1:end_row]

    for i, row in enumerate(rows, start=start_row):
        if any(date_to_match.lower() in cell.lower() for cell in row):
            print(f"Content: {row}")
            if row[3] == '' and row[5] == '':
                print(f"Match found in row {i}. Inserting content.")
                worksheet.update_cell(i, 2, "4T")
                worksheet.update_cell(i, 4, version)
                worksheet.update_cell(i, 6, success_percentage)
                return True
            print(f"Row {i} with date {date_to_match} does not meet the insertion conditions. Trying next empty row.")
            continue
    print(f"No match found for date {date_to_match}.")
    return False

# print(f"Title: {worksheet.title}, ID: {worksheet.id}, URL: {worksheet.url}")

# if insert_content_matching_date(FIRST_START_ROW, FIRST_END_ROW, current_date):
#     print("Content inserted in the first part.")
# else:
#     print("No match found in the first part.")


if insert_content_matching_date(SECOND_SYART_ROW, SECOND_END_ROW, current_date	):
    print("Content inserted in the second part.")
else:
    print("No match found in the second part.")
