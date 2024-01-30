from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import os, time

# Load .env file
from dotenv import load_dotenv
load_dotenv()

# Start browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login():
    # Fill username and password
    driver.find_element(By.ID, "userid").send_keys(os.getenv("NIM"))
    driver.find_element(By.ID, "password").send_keys(os.getenv("PASSWORD"))

    # Click login button
    driver.find_element(By.NAME, "login").click()

def afterLogin():
    # Click on a#link-kuesioner
    driver.find_element(By.CSS_SELECTOR, "a#link-kuesioner").click()

    # Fine .role_box and click the first div
    driver.find_element(By.CSS_SELECTOR, "div.role_box").click()

# Open URL
driver.get("https://qa.unair.ac.id/qa/gate/login")

# Login
login()
afterLogin()

# Get all selects
selects = ["select#idmk", "select#dosen", "select#idunit"]

while True:
    # Check if logged out by seeing if there is any element with id=userid
    try:
        driver.find_element(By.ID, "userid")
        login()
        afterLogin()
    except:
        pass

    # Check if there is any kuesioner to be filled
    to_be_filled = driver.find_elements(By.CSS_SELECTOR, "a.card-link")
    if len(to_be_filled) == 0:
        print("No kuesioner left to be filled")
        break

    # Get the first a.card_link
    to_be_filled[0].click()

    # Loop over `selects`, if there is any in the page
    # then select the first option
    for s in selects:
        # If the select is select#dosen, then wait for 1 second
        # so it can load the options
        if s == "select#dosen":
            time.sleep(0.5)

        try:
            element = driver.find_element(By.CSS_SELECTOR, s)
            element.click()

            select = Select(element)
            select.select_by_index(1)
        except:
            pass

    # Select all input with 134 as the value
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[value='134']")
    for i in inputs:
        i.click()

    # Click on button.ibtn
    driver.find_element(By.CSS_SELECTOR, "button.ibtn").click()

    try:
        # Confirm the alert
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    # Go back to the previous page
    driver.get("https://qa.unair.ac.id/qa/kuesioner/dashboard")

# End of the program
input("Press enter to exit ;)")