import requests as rq
import os

SHEET_URL = "https://api.sheety.co/6245f7e354a5acb534670c176d303777/flightDeals/sheet1"
BEARER_KEY = os.environ["SHEETLY_BEARER_KEY"]

SHEETLY_HEADERS = {
    "Authorization": f"Bearer {BEARER_KEY}"
}


def fetch_sheet():
    sheet_request = rq.get(url=SHEET_URL, headers=SHEETLY_HEADERS)
    sheet_request.raise_for_status()
    sheet_data = sheet_request.json()["sheet1"]
    return sheet_data


class DataManager:
    def __init__(self):
        self.criteria_data = fetch_sheet()

    def update_sheet(self):
        current_sheet = fetch_sheet()
        if current_sheet != self.criteria_data:
            print("Current sheet is different from criteria data. Updating sheet...")
            for i in range(len(self.criteria_data)):
                row = self.criteria_data[i]
                print(f"Checking if row {row['id']} needs updating...")
                if i > (len(current_sheet) - 1) or current_sheet[i] != row:
                    print(f"Updating row {row['id']}...")
                    send_data = {
                        "sheet1": row
                    }
                    update_request = rq.put(url=f"{SHEET_URL}/{row['id']}",
                                            json=send_data,
                                            headers=SHEETLY_HEADERS)
                    update_request.raise_for_status()
                else:
                    print("Same row, no need to update.")
        else:
            print("Sheet is same to criteria data. No need to update sheet.")
