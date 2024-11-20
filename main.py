import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_logging_directory():
    """Create logs directory if it doesn't exist"""
    if not os.path.exists("logs"):
        os.makedirs("logs")
        logger.info("Created logs directory")


def verify_title(driver):
    try:
        logger.info(f"Starting title verification test using {driver.name}")
        # Navigate to the website
        url = "https://www.canva.com/design/DAF8D5PfEz0/ocjnH2CvH74Gmhu7hU3iMg/edit"
        logger.info(f"Navigating to URL: {url}")
        driver.get(url)
        # Get the title and verify it
        title = driver.title
        expected_title = "LAUNCHING THE NEW EDITION COFFEE SHOP - Website"
        logger.info(f"Actual title: {title}")
        logger.info(f"Expected title: {expected_title}")
        if title == expected_title:
            logger.info(f"Title verification successful on {driver.name}!")
        else:
            logger.warning(
                f"Title verification failed on {driver.name}. "
                f"Expected '{expected_title}', but got '{title}'."
            )
    except Exception as e:
        logger.error(f"An error occurred during title verification: {str(e)}", exc_info=True)
    finally:
        logger.info("Closing browser")
        driver.quit()


if __name__ == "__main__":
    setup_logging_directory()
    # Setup Firefox options
    firefox_options = FirefoxOptions()
    firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    logger.info("Firefox options configured")
    # Correct path to geckodriver
    gecko_driver_path = r"C:\GeckoDriver\geckodriver.exe"
    try:
        logger.info("Initializing Firefox WebDriver...")
        firefox_driver = webdriver.Firefox(
            service=FirefoxService(executable_path=gecko_driver_path),
            options=firefox_options
        )
        logger.info("Firefox WebDriver initialized successfully")
        # Perform title verification
        verify_title(firefox_driver)
    except Exception as e:
        logger.error(f"Failed to initialize Firefox WebDriver: {str(e)}", exc_info=True)