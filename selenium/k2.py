from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def main(port):
    driver = webdriver.Firefox()

    try:
        # Open the Streamlit app
        driver.get(f"http://localhost:{port}/k2")  # Replace with the actual URL of your Streamlit app
        driver.maximize_window() # For maximizing window

        time.sleep(5)

    finally:
        # Close the browser
        driver.quit()
