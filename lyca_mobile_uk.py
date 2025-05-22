from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import time
import pandas as pd

# Define the list of URLs you want to scrape
urls = [
    "https://www.lycamobile.co.uk/paymonthly/en/product-listing/24-month-plan",
    "https://www.lycamobile.co.uk/paymonthly/en/product-listing/12-month-plan",
    "https://www.lycamobile.co.uk/paymonthly/en/product-listing/1-month-plan"
]

# Create a driver instance
driver = webdriver.Chrome()

# Final data list
data = []

# Loop through each URL
for url in urls:
    print(f"Scraping: {url}")
    driver.get(url)
    time.sleep(3)

    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Replace this with the actual button class used on the site
            load_more_button = driver.find_element(By.CLASS_NAME, "load-more-btn")  # <-- Replace if needed
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(1)
            load_more_button.click()
            print("Clicked 'Load More' button")
            time.sleep(3)

        except NoSuchElementException:
            print("No more 'Load More' button found.")
            break
        except ElementClickInterceptedException:
            print("Click intercepted — retrying...")
            time.sleep(2)

    # Parse this page's content
    soup = BeautifulSoup(driver.page_source, "html.parser")
    product_blocks = soup.find_all("div", class_="card-body mx-1 mx-lg-2")

    for product_block in product_blocks:
        # Extract product details
        product_description_block = product_block.find("p", class_="color-87909F mt-3 fs-16 mb-2 font-family-Regular")
        product_description = product_description_block.text.strip() if product_description_block else 'None'
        # Extract actual price
        actual_price_block = product_block.find("s")        
        actual_price = actual_price_block.text.strip() if actual_price_block else 'None'
        # Extract purchase price
        purchase_price_block = product_block.find("span", class_="fs-28 ng-star-inserted")
        purchase_price = purchase_price_block.text.strip() if purchase_price_block else 'None'
        # Extract data offered
        data_block = product_block.find("span", class_="plans-data-volume font-family-Bold")
        data_offered = data_block.text.strip() if data_block else 'None'
        # Extract product features
        features_list_block = product_block.find_all("li", class_="text-87909F mt-1 fs-16 fs-sm-13 font-family-Regular ng-star-inserted")
        features = [li.text.strip() for li in features_list_block] if features_list_block else ['None']
        # Extract offer details
        offer_block = product_block.find("span", class_="fs-16 font-family-Regular ng-star-inserted")
        offer = offer_block.text.strip() if offer_block else 'None'
        data.append({
            "url": url,
            "description": product_description,
            "actual_price": actual_price,
            "purchase_price": purchase_price,
            "data_offered": data_offered,
            "features": features,
            "offer": offer
        })
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(data)
print(df)
df.to_csv("lycamobile_products.csv", index=False)