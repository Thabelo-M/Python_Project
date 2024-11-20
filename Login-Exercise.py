#Defining the Modules
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Configure the Webdriver
driver = webdriver.Firefox()

#Set the URL of the login page
LOGIN_URL = "https://the-internet.herokuapp.com/login"

#Define your test cases for login using Python Tuples(used to store multiple items in a single variable.)
test_cases = [
    #Correct username and wrong password
    ("tomsmith", "wrong_pass", "Your password is invalid!"),
    #Correct username and correct password
    ("tomsmith", "SuperSecretPassword!", "You logged into a secure area!"),
    #Wrong username and correct password
    ("thomas", "SuperSecretPassword!", "Your username is invalid!"),
    #Empty username and empty password
    ("", "", "Your username is invalid!"),
    #Empty username and correct password
    ("", "SuperSecretPassword!", "Your username is invalid!")
]

#Utilise the pytest
@pytest.mark.parametrize("username, password, expected", test_cases)
#Define your function
def test_login(username, password, expected):
    driver.get(LOGIN_URL)

    #Locate the input fields
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    #Clear the fields and enter new testdata
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)

    #Make the submit button to be responsive (using python wait)
    login_button.click()
    time.sleep(2.5)

    #Check the results
    if "secure" in driver.current_url:
        message = driver.find_element(By.CSS_SELECTOR, ".flash.success").text.strip().replace("\n", "").replace("×", "")
    else:
        message = driver.find_element(By.CSS_SELECTOR, ".flash.error").text.strip().replace("\n", "").replace("×", "")

    #Assert the expected results
    assert expected.split(",")[0] in message, f"Expected '{expected}', but got '{message}'"

#Close the webdriver
@pytest.fixture(scope="session", autouse=True)
def teardown():
    yield
    driver.quit()