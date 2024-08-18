# otpauth://totp/Twitter:@YOUR_USERNAME?secret=YOUR_SECRET&issuer=Twitter

from dotenv import load_dotenv
import os
import pyotp
from playwright.sync_api import Playwright, sync_playwright, expect
import time
load_dotenv()

username = os.getenv('MY_USERNAME')
password = os.getenv('PASSWORD')
secret = os.getenv('SECRET')

post_text = "How to get rich\n\n\n1. Stay out of debt\n2. Save\n3. Invest"


# function to generate OTP
def generate_otp(secret):
    secret = secret
    totp = pyotp.TOTP(secret)
    current_otp = totp.now()
    return current_otp

#main function

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(50000)
    page.goto("https://twitter.com/login")
    page.get_by_label("Phone, email, or username").fill(f"{username}")
    time.sleep(2)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill(f"{password}")
    time.sleep(2)
    page.get_by_test_id("LoginForm_Login_Button").click()
    page.get_by_test_id("ocfEnterTextTextInput").click()
    otp = generate_otp(secret)
    page.get_by_test_id("ocfEnterTextTextInput").fill(f"{otp}")
    time.sleep(2)
    page.get_by_test_id("ocfEnterTextNextButton").click()
    page.get_by_test_id("tweetTextarea_0").fill(f"{post_text}")
    page.get_by_test_id("tweetButtonInline").click()

    time.sleep(20)
    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)