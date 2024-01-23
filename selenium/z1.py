from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()

try:
    # Open the Streamlit app
    driver.get("http://localhost:8501/z1")  # Replace with the actual URL of your Streamlit app
    driver.maximize_window() # For maximizing window

    time.sleep(3)

    next_page = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[14]/div[3]/div[1]/div[1]/div[1]/div[1]/button[1]")
    next_page.click()
    time.sleep(1)

    preview = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]/div[1]/p[1]")
    preview.click()
    time.sleep(1)

    x = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[2]/div[1]/button[1]")
    x.click()
    time.sleep(1)

    edit = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/button[1]/div[1]/p[1]")
    edit.click()
    time.sleep(1)

    x = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/span[2]/*[name()='svg'][1]")
    x.click()
    time.sleep(1)

    save = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[5]/div[1]/button[1]/div[1]/p[1]")
    save.click()
    time.sleep(1)

    delete = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[5]/div[3]/div[1]/div[1]/div[1]/div[1]/button[1]/div[1]/p[1]")
    delete.click()
    time.sleep(1)

    button = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/*[name()='svg'][1]")
    button.click()
    time.sleep(1)
    
    option = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/li[1]/div[1]/div[1]/div[1]")
    option.click()
    time.sleep(1)

    button = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/*[name()='svg'][1]")
    button.click()
    time.sleep(1)

    confirm = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[4]/div[1]/button[1]")
    confirm.click()
    time.sleep(1)
    
    x = driver.find_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[2]/div[1]/button[1]")
    x.click()
    time.sleep(1)


finally:
    # Close the browser
    driver.quit()
