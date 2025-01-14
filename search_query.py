from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tavily import TavilyClient
import time
import os
from dotenv import load_dotenv
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

def search_myntra_for_query(key):  
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_products = []  # List to store scraped data
    # Search for the query in Google Shopping (via Tavily Client)
    answer = tavily_client.search(query=f"{key} site:myntra.com", search_depth="basic")
    url = answer["results"][0]["url"]

    # Open the URL
    driver.get(url)

    # Wait for the page to load completely
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Scroll down multiple times to load more products
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down
        time.sleep(3)  # Wait for content to load

    # Wait for product elements to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'product-base')]"))
    )

    # Get the product elements
    products = driver.find_elements(By.XPATH, "//li[contains(@class, 'product-base')]")

    # Scrape product data
    for product in products:  # Scrape only the first 5 products
        brand = product.find_element(By.XPATH, ".//h3[contains(@class, 'product-brand')]").text
        name = product.find_element(By.XPATH, ".//h4[contains(@class, 'product-product')]").text
        price = product.find_element(By.XPATH, ".//div[contains(@class, 'product-price')]").text
        link = product.find_element(By.XPATH, ".//a[@data-refreshpage='true']").get_attribute("href")

            # Append the scraped data to product_data
        all_products.append({
            "brand": brand,
            "name": name,
            "price": price,
            "link": link,
        })
    
    driver.quit()  # Ensure the driver quits even if there's an error

    return all_products