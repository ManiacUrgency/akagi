import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_redirected_url(google_news_url):
    # Set up Chrome options to run in headless mode (no GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

    # Specify the path to your ChromeDriver
    service = ChromeService(executable_path='/Users/stephenjin/Dev/chrome-driver/chromedriver-mac-arm64/chromedriver')  # Replace with your path

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the Google News URL
        driver.get(google_news_url)

        # Wait for the final URL to load; no need to load full page content
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        current_url = driver.current_url

        print("waiting start")
        while True:
            print(current_url)
            if "news.google.com" not in current_url:
                break
            time.sleep(0.5)
            current_url = driver.current_url
        print("waiting end")

        # Get the final redirected URL
        final_url = driver.current_url

        print("final url:", final_url)
        #time.sleep(5)

        return final_url
    finally:
        # Close the browser
        driver.quit()

# Example usage
google_news_url = "https://news.google.com/rss/articles/CBMitAFBVV95cUxNaU04bk1JTFZFZGloWFhXVlB0R0Y1cFpSbWJQYklrMXhrbXBFdnFrNkFNcE9raThYYWw4SEFmcENoTE5lNy0wOVBaTWJmay1wR0xOQUpRblU5cWpmV3VGbGZrblotYkNtQVlfX0tIczI2eGQ4VjBoNUl4VmVDcGlLV05BQ1hDQUdJOVZPdy13SlVfUW9kbklUdnh3MHhPOXpRaE0wekxTeklKdk40UG5wd3dlTDPSAboBQVVfeXFMT2o0TWZ5RmE0R0pRSjVJckVGOS1OenZsQ1BHdzB5NnJpdl9tckVUQm9XRGhrTGYxSV9UeUtuX0dHNmJESFdRUjNfRVJUX0ZzQXB1bVV3TlF5dVo3VDRxa3hlOVl3dUdZVjhmYUw4cXFIcm4yRUNudGFtTkdnU1BrazBxc0RJZlAyU0gyNXdSZ25MTTFYNHUwWm9rbk5Sa0l0dzZYZmRwcnZzdEc1aXJFUlJWVEl0NlpFTGFn?oc=5&hl=en-US&gl=US&ceid=US:en"
redirected_url = get_redirected_url(google_news_url)
print("Final Redirected URL:", redirected_url)
