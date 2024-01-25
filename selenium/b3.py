from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def main(port):
    driver = webdriver.Firefox()

    try:
        # Open the Streamlit app
        driver.get(f"http://localhost:{port}/b3")  # Replace with the actual URL of your Streamlit app
        driver.maximize_window() # For maximizing window

        time.sleep(3)

        ret = driver.find_element("xpath",
                                      "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]/div[1]/p[1]")
        ret.click()
        time.sleep(1)

        ret = driver.find_element("xpath",
                                  "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[11]/div[1]/button[1]")
        ret.click()
        time.sleep(1)

        ret = driver.find_element("xpath",
                                      "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]/div[1]/p[1]")
        ret.click()
        time.sleep(1)

        approve = driver.find_element("xpath",
                                      "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[11]/div[1]/button[1]/div[1]/p[1]")
        approve.click()
        time.sleep(1)

        penalty = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/button[1]/div[1]/p[1]")
        penalty.click()
        time.sleep(1)

        ret = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[11]/div[1]/button[1]/div[1]/p[1]")
        ret.click()
        time.sleep(1)

        penalty = driver.find_element("xpath",
                                      "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/button[1]/div[1]/p[1]")
        penalty.click()
        time.sleep(1)

        approve = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[6]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[11]/div[1]/button[1]/div[1]/p[1]")
        approve.click()
        time.sleep(1)








    finally:
        # Close the browser
        driver.quit()
