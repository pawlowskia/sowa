from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def main(port):
    driver = webdriver.Firefox()

    try:
        # Open the Streamlit app
        driver.get(f"http://localhost:{port}/b1")  # Replace with the actual URL of your Streamlit app
        driver.maximize_window() # For maximizing window

        time.sleep(3)

        prepare = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[4]/div[1]/button[1]/div[1]/p[1]")
        prepare.click()

        time.sleep(1)
        prepare2 = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]/div[3]/div[1]/button[1]/div[1]/p[1]")
        prepare2.click()

    finally:
        # Close the browser
        driver.quit()
