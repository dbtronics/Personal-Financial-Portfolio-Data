from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import csv
import os

def get_psx_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://dps.psx.com.pk", timeout=60000)
        print("Successfully accessed PSX Data Portal")
        if page.query_selector("button.tingle-modal__close"):
            page.click("button.tingle-modal__close")
        # Select "All" from the dropdown to show all data entries
        page.select_option("select[name='DataTables_Table_0_length']", value='-1')
        time.sleep(2)  # Give time for table to refresh
        print("All data entries for regular market have been selected")


        # Extract all rows of the main table
        rows = page.query_selector_all("table#DataTables_Table_0 tbody tr")

        for row in rows:
            cells = row.query_selector_all("td")
            data = {
                "SYMBOL": cells[0].inner_text().strip(),
                "LDCP": cells[1].inner_text().strip(),
                "OPEN": cells[2].inner_text().strip(),
                "HIGH": cells[3].inner_text().strip(),
                "LOW": cells[4].inner_text().strip(),
                "CURRENT": cells[5].inner_text().strip(),
                "CHANGE": cells[6].inner_text().strip(),
                "CHANGE (%)": cells[7].inner_text().strip(),
                "VOLUME": cells[8].inner_text().strip(),
                "DATE EXTRACTED": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            print(data)

            csv_file = "psx_market_data.csv"
            # Convert numeric fields to float where possible
            for key in ["LDCP", "OPEN", "HIGH", "LOW", "CURRENT", "CHANGE", "CHANGE (%)", "VOLUME"]:
                try:
                    data[key] = float(data[key].replace(',', '').replace('%', ''))
                except ValueError:
                    pass  # Keep as is if conversion fails
            headers = ["SYMBOL", "LDCP", "OPEN", "HIGH", "LOW", "CURRENT", "CHANGE", "CHANGE (%)", "VOLUME", "DATE EXTRACTED"]

            file_exists = os.path.isfile(csv_file)
            with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
        
        print(f"Data successfully written to {csv_file}")

        
        browser.close()

# Example usage
if __name__ == "__main__":
    get_psx_data()