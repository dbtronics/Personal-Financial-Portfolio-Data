import requests
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
import sys

load_dotenv()

def get_headers(api_token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f"Bearer {api_token}",
        'origin': 'https://www.blossomsocial.com',
        'priority': 'u=1, i',
        'referer': 'https://www.blossomsocial.com/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-preferred-currency': 'CAD',
        'x-request-id': 'WEB_E01A37A50ED0438FBEC0',
        'x-self-user-id': 'FL3pGHNPsKpDgBne',
        'x-user-agent': 'com.blossomsocial.web',
        'x-version-id': '1.0.0',
    }

if len(sys.argv) < 2:
    print("Usage: python data-automation-asb-portfolio-api.py <BEARER_TOKEN>")
    sys.exit(1)

API_TOKEN = sys.argv[1]
headers = get_headers(API_TOKEN)

CSV_FILE = 'blossom_portfolio_data.csv'
HEADERS = [
    'Account Type',
    'Broker Name',
    'User Broker Name',
    'Organization Name',
    'Investment ID',
    'Investment Type',
    'Exchange',
    'Current Price',
    'Average Buy Price',
    'ETF Provider',
    'Holding',
    'Portfolio Percent',
    'Quantity',
    'Percent Change (All Time)',
    'Percent Change (Day)',
    'Percent Change (YTD)',
    'Value Change (All Time)',
    'Value Change (Day)',
    'Value Change (YTD)',
    'Date Extracted'
]


def extract_portfolio_data():
    response = requests.get(
        f"{os.getenv('API_ENDPOINT')}",
        headers=headers,
    )
    if response.status_code == 200:
        # print(response.text)
        data = response.json()
        account_investment_list = data.get('accountInvestmentList', [])
        print("Number of elements in accountInvestmentList:", len(account_investment_list))
        for account in account_investment_list:
            account_index = account_investment_list.index(account)
            account_type = account.get('accountType')
            broker_name = account.get('brokerName')
            user_broker_name = account.get('userBrokerName')

            print()
            print(f"accountType: {account_type}, \tbrokerName: {broker_name}, \tuserBrokerName: {user_broker_name}")
            
            current_investments = account.get('currentInvestmentList', [])

            for investment in current_investments:
                investment_id = investment.get('investmentId')
                investment_type = investment.get('investmentType')
                exchange = investment.get('exchange')
                current_price = investment.get('currentPrice')
                average_buy_price = investment.get('averageBuyPrice')
                etf_provider = investment.get('etfProvider')
                holding = investment.get('holding')
                organisation_name = investment.get('organisationName')
                portfolio_percent = investment.get('portfolioPercent')
                quantity = investment.get('quantity')
                print(f"organisationName: {organisation_name}")
                print(f"investmentId: {investment_id}")
                print(f"investmentType: {investment_type}")
                print(f"exchange: {exchange}")
                print(f"currentPrice: {current_price}")
                print(f"averageBuyPrice: {average_buy_price}")
                print(f"etfProvider: {etf_provider}")
                print(f"holding: {holding}")
                print(f"portfolioPercent: {portfolio_percent}")
                print(f"quantity: {quantity}")

                percent_change = investment.get('percentChange', [])
                value_change = investment.get('valueChange', [])

                percent_all_time = percent_change.get('allTime')
                percent_day = percent_change.get('day')
                percent_ytd = percent_change.get('yearToDate')
                value_all_time = value_change.get('allTime')
                value_day = value_change.get('day')
                value_ytd = value_change.get('yearToDate')
                print(f"percent_all_time: {percent_all_time}")
                print(f"percent_day: {percent_day}")
                print(f"percent_ytd: {percent_ytd}")
                print(f"value_all_time: {value_all_time}")
                print(f"value_day: {value_day}")
                print(f"value_ytd: {value_ytd}")

                date_extracted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Write header only if file does not exist or is empty
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        account_type,
                        broker_name,
                        user_broker_name,
                        organisation_name,
                        investment_id,
                        investment_type,
                        exchange,
                        current_price,
                        average_buy_price,
                        etf_provider,
                        holding,
                        portfolio_percent,
                        quantity,
                        percent_all_time,
                        percent_day,
                        percent_ytd,
                        value_all_time,
                        value_day,
                        value_ytd,
                        date_extracted
                    ])
            print()
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

if __name__ == "__main__":
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)
    extract_portfolio_data()