import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
from pymongo import MongoClient
import config

def get_new_proxy():
    response = requests.get(f"https://proxymesh.com/api/proxies", auth=(config.PROXYMESH_USERNAME, config.PROXYMESH_PASSWORD))
    proxies = response.json().get('data')
    return proxies[0]['url']

def scrape_trending_topics(proxy):
    # Specify the path to the ChromeDriver executable
    chrome_driver_path = 'C:/Users/abc/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'  # Update this path as needed

    # Initialize the ChromeDriver service
    service = Service(executable_path=chrome_driver_path)

    # Optional: Specify Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    # Uncomment the line below to run Chrome in headless mode
    # chrome_options.add_argument("--headless")

    # Initialize the WebDriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://twitter.com/login")

        username = driver.find_element(By.NAME, "session[username_or_email]")
        password = driver.find_element(By.NAME, "session[password]")
        username.send_keys(config.TWITTER_USERNAME)
        password.send_keys(config.TWITTER_PASSWORD)
        password.send_keys(Keys.RETURN)
        sleep(5)

        driver.get("https://twitter.com/home")
        sleep(5)
        trending_section = driver.find_element(By.XPATH, '//section[@aria-labelledby="accessible-list-0"]')
        trends = trending_section.find_elements(By.XPATH, './/span[contains(text(), "#")]')
        top_trends = [trend.text for trend in trends[:5]]
    finally:
        driver.quit()

    return top_trends

def store_data(trends, proxy):
    client = MongoClient(config.MONGO_URI)
    db = client['twitter_scraping']
    collection = db['trending_topics']
    data = {
        "unique_id": str(uuid.uuid4()),
        "trends": trends,
        "timestamp": datetime.now(),
        "proxy": proxy
    }
    collection.insert_one(data)
    return data

def fetch_trending_data():
    proxy = get_new_proxy()
    trends = scrape_trending_topics(proxy)
    data = store_data(trends, proxy)
    return data



# # scraper.py
# import uuid
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from time import sleep
# import requests
# from pymongo import MongoClient
# import config

# def get_new_proxy():
#     response = requests.get(f"https://proxymesh.com/api/proxies", auth=(config.PROXYMESH_USERNAME, config.PROXYMESH_PASSWORD))
#     proxies = response.json().get('data')
#     return proxies[0]['url']

# def scrape_trending_topics(proxy):
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument(f'--proxy-server={proxy}')
#     driver = webdriver.Chrome(options=chrome_options)

#     driver.get("https://twitter.com/login")

#     username = driver.find_element(By.NAME, "session[username_or_email]")
#     password = driver.find_element(By.NAME, "session[password]")
#     username.send_keys(config.TWITTER_USERNAME)
#     password.send_keys(config.TWITTER_PASSWORD)
#     password.send_keys(Keys.RETURN)
#     sleep(5)

#     driver.get("https://twitter.com/home")
#     sleep(5)
#     trending_section = driver.find_element(By.XPATH, '//section[@aria-labelledby="accessible-list-0"]')
#     trends = trending_section.find_elements(By.XPATH, './/span[contains(text(), "#")]')
#     top_trends = [trend.text for trend in trends[:5]]
#     driver.quit()
#     return top_trends

# def store_data(trends, proxy):
#     client = MongoClient(config.MONGO_URI)
#     db = client['twitter_scraping']
#     collection = db['trending_topics']
#     data = {
#         "unique_id": str(uuid.uuid4()),
#         "trends": trends,
#         "timestamp": datetime.now(),
#         "proxy": proxy
#     }
#     collection.insert_one(data)
#     return data

# def fetch_trending_data():
#     proxy = get_new_proxy()
#     trends = scrape_trending_topics(proxy)
#     data = store_data(trends, proxy)
#     return data


# # # scraper.py
# # import uuid
# # from datetime import datetime
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# # from time import sleep
# # import requests
# # from pymongo import MongoClient
# # import config

# # def get_new_proxy():
# #     response = requests.get(f"https://proxymesh.com/api/proxies", auth=(config.PROXYMESH_USERNAME, config.PROXYMESH_PASSWORD))
# #     proxies = response.json().get('data')
# #     return proxies[0]['url']

# # def scrape_trending_topics():
# #     driver = webdriver.Chrome()
# #     driver.get("https://twitter.com/login")

# #     username = driver.find_element(By.NAME, "session[username_or_email]")
# #     password = driver.find_element(By.NAME, "session[password]")
# #     username.send_keys(config.TWITTER_USERNAME)
# #     password.send_keys(config.TWITTER_PASSWORD)
# #     password.send_keys(Keys.RETURN)
# #     sleep(5)

# #     driver.get("https://twitter.com/home")
# #     sleep(5)
# #     trending_section = driver.find_element(By.XPATH, '//section[@aria-labelledby="accessible-list-0"]')
# #     trends = trending_section.find_elements(By.XPATH, './/span[contains(text(), "#")]')
# #     top_trends = [trend.text for trend in trends[:5]]
# #     driver.quit()
# #     return top_trends

# # def scrape_with_proxy():
# #     proxy = get_new_proxy()
# #     chrome_options = webdriver.ChromeOptions()
# #     chrome_options.add_argument(f'--proxy-server={proxy}')
# #     driver = webdriver.Chrome(options=chrome_options)
# #     trends = scrape_trending_topics()
# #     driver.quit()
# #     return trends

# # def store_data(trends):
# #     client = MongoClient(config.MONGO_URI)
# #     db = client['twitter_scraping']
# #     collection = db['trending_topics']
# #     data = {
# #         "unique_id": str(uuid.uuid4()),
# #         "trends": trends,
# #         "timestamp": datetime.now()
# #     }
# #     collection.insert_one(data)
