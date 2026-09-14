import requests
import csv
import sys
from io import StringIO
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from Config.settings import get_google_sheet_csv_url


def fetch_sheet():
    csv_url = get_google_sheet_csv_url()

    response = requests.get(csv_url)

    response.raise_for_status()

    csv_data = StringIO(response.text)

    reader = csv.DictReader(csv_data)

    rows = list(reader)

    return rows


def main():

    rows = fetch_sheet()

    print("Rows fetched:", len(rows))

    for r in rows[:3]:
        print(r)


if __name__ == "__main__":
    main()
