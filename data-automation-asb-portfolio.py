from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def get_blossom_portfolio_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.blossomsocial.com/login")
        
        email = os.getenv("BLOSSOM_EMAIL") 
        password = os.getenv("BLOSSOM_PASSWORD")
        
        page.fill('input[type="email"]', email)
        page.fill('input[type="password"]', password)
        page.keyboard.press("Enter")
        time.sleep(5)  # Wait for login to complete
        print("Successfully logged into Blossom Social")
        # page.click('div[data-sidebar="content"] > ul[data-sidebar="menu"] > li:nth-child(4) > div')
        page.click("span:text('Portfolio')")
        print("Navigated to Portfolio page")
        time.sleep(5)  # Wait for the portfolio page to load
        content = page.content()

        # Extract all rows of the portfolio table
        rows = page.query_selector_all("table > tbody > tr")
        extracted_data = []

        for row in rows:
            try:
                holding_symbol = row.query_selector("td:nth-child(1) span.font-semibold").inner_text()  # simpler, less fragile
            except:
                holding_symbol = ""
            
            try:
                holding_name = row.query_selector("td:nth-child(1) span.text-secondary-text").inner_text()
            except:
                holding_name = ""

            try:
                percent_of_portfolio = row.query_selector("td:nth-child(2).text-right.font-semibold").inner_text()  # simplified
            except:
                percent_of_portfolio = ""

            try:
                position = row.query_selector("td:nth-child(3) > div > span").inner_text()
            except:
                position = ""

            try:
                total_share = row.query_selector("td:nth-child(3) > div > div").inner_text()
            except:
                total_share = ""

            try:
                element = row.query_selector("td:nth-child(4) > div > span.text-base.font-semibold.text-primary-green") or row.query_selector("td:nth-child(4) > div > span.text-base.font-semibold.text-primary-red")
                return_today_dollar = element.inner_text() if element else ""
            except:
                return_today_dollar = ""

            try:
                element = row.query_selector("td:nth-child(4) > div > span.text-sm.font-semibold.text-primary-green") or row.query_selector("td:nth-child(4) > div > span.text-sm.font-semibold.text-primary-red")
                return_today_percent = element.inner_text() if element else ""
            except:
                return_today_percent = ""

            try:
                element = row.query_selector("td:nth-child(5) > div > span.text-base.font-semibold.text-primary-green") or row.query_selector("td:nth-child(5) > div > span.text-base.font-semibold.text-primary-red")
                return_all_time_dollar = element.inner_text() if element else ""
            except:
                return_all_time_dollar = ""

            try:
                element = row.query_selector("td:nth-child(5) > div > span.text-sm.font-semibold.text-primary-green") or row.query_selector("td:nth-child(5) > div > span.text-sm.font-semibold.text-primary-red")
                return_all_time_percent = element.inner_text() if element else ""
            except:
                return_all_time_percent = ""

            # Clean up the extracted data
            percent_of_portfolio = percent_of_portfolio.replace('%', '')
            position = position.replace('$', '')
            total_share = total_share.replace('shares', '').strip()
            return_today_dollar = return_today_dollar.replace('$', '')
            return_today_percent = return_today_percent.replace('%', '')
            return_all_time_dollar = return_all_time_dollar.replace('$', '')
            return_all_time_percent = return_all_time_percent.replace('%', '')
            
            try:
                current_price = float(position) / float(total_share) if total_share and position else 0
            except:
                current_price = 0

            # Append the cleaned data to the list
            extracted_data.append([
                holding_symbol,
                holding_name,
                percent_of_portfolio,
                position,
                total_share,
                current_price, 
                return_today_dollar,
                return_today_percent,
                return_all_time_dollar,
                return_all_time_percent
            ])

        for row in extracted_data:
            print(row)
        print("Extracted data from Blossom Portfolio")

        headers = [
            "Holding Symbol",
            "Holding Name",
            "% of Portfolio",
            "Position",
            "Total Shares",
            "Current Price",
            "Today's Return ($)",
            "Today's Return (%)",
            "All-time Return ($)",
            "All-time Return (%)"
        ]

        output_file = "blossom_portfolio.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(extracted_data)
        print(f"Data successfully written to {output_file} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        browser.close()
        return content
    
if __name__ == "__main__":
    get_blossom_portfolio_data()