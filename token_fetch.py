from playwright.sync_api import sync_playwright
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Global holder for the token
token_holder = {"token": None}

# Define handler globally so it can be reused or tested
def handle_request(request):
    url = request.url
    if url.startswith("https://ci2q6uhqok.execute-api.ca-central-1.amazonaws.com/prod/portfolio/portfolio_and_investments"):
        auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
        if auth_header and "Bearer" in auth_header:
            token_holder["token"] = auth_header.split("Bearer ")[1]
            print("✅ Bearer Token Captured:", token_holder["token"])

def get_bearer_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.on("request", handle_request)
        page = context.new_page()
        
        # Navigate to Blossom Social login page
        page.goto("https://www.blossomsocial.com/login")
        
        email = os.getenv("BLOSSOM_EMAIL") 
        password = os.getenv("BLOSSOM_PASSWORD")
        
        page.fill('input[type="email"]', email)
        page.fill('input[type="password"]', password)
        page.keyboard.press("Enter")
        time.sleep(5)  # Wait for login to complete
        print("Successfully logged into Blossom Social")
        
        # Navigate to Portfolio page
        page.click("span:text('Portfolio')")
        print("Navigated to Portfolio page")
        # time.sleep(5)  # Wait for the portfolio page to load
        # content = page.content()

        # Wait for the token to be captured
        print("⏳ Waiting for network request to portfolio endpoint...")
        time.sleep(5)  # Increase if needed depending on network speed

        browser.close()
        return token_holder["token"]

# Use the function
bearer_token = get_bearer_token()
print("🔑 Final Bearer Token:", bearer_token)