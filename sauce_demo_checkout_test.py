#Modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time

#Define the constants
BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

#Test how to add product to the cart and completing checkout
def test_add_to_cart_and_checkout():
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
#Write the test cases
    try:
       #Test case 1: Open the website
       driver.get(BASE_URL)
       print("Opened website:", BASE_URL)

       #Test case 2: Login
       WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.ID, "user-name"))
       ).send_keys(USERNAME)
       driver.find_element(By.ID, "password").send_keys(PASSWORD)
       driver.find_element(By.ID, "login-button").click()
       print("Logged in successfully!")

       #Test case 3: Add the 1st product to the cart
       WebDriverWait(driver, 10).until(
           EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn_inventory')]"))
       ).click()
       print("Added to cart.")

       #Test case 4: Navigate to the cart
       driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
       print("Opened the shopping cart.")

       #Test case 5: Verify that the cart has a product
       cart_items =  WebDriverWait(driver, 10).until(
           EC.presence_of_all_elements_located((By.CLASS_NAME,"cart_item"))
       )
       assert len(cart_items) > 0, "The cart is empty"
       print(f"Cart contains {len(cart_items)} item(s)")

       #Test case 6: Proceed to checkout
       driver.find_element(By.ID, "checkout").click()
       print("Proceed to 'checkout'")

       #Test case 7: Enter checkout information
       WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.ID, "first-name"))
       ).send_keys("Demo")
       driver.find_element(By.ID, "last-name").send_keys("User")
       driver.find_element(By.ID, "postal-code").send_keys("12345")
       driver.find_element(By.ID, "continue").click()
       print("Enter your details to checkout and click 'continue'.")

       #Test case 8: Complete checkout
       WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.ID, "finish"))
       ).click()
       print("click 'complete' to checkout.")

       #Test case 9: Verify the item checkout
       confirmation_message = WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
       ).text
       assert "THANK YOU FOR YOUR ORDER" in confirmation_message.upper(), "checkout failed"
       print("Order completed", confirmation_message)
       #Pause
       time.sleep(3)
    finally:
        driver.quit()
        print("Testing done and browser closed!")

if __name__ =="__main__":
    test_add_to_cart_and_checkout()
