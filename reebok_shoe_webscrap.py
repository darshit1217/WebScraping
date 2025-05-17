from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
import time
import pandas as pd

# Start browser
driver = webdriver.Chrome()
driver.get("https://reebok.abfrl.in/c/men-sale-footwear")
time.sleep(3)  # Allow initial load

# Loop until all products are loaded
while True:
    try:
        # Scroll to bottom to make "Load More" button visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Try to find and click the "Load More" button
        load_more_button = driver.find_element(By.CLASS_NAME, "XYZ")  # Replace XYZ with actual button class
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(1)
        load_more_button.click()
        print("Clicked 'Load More' button")
        time.sleep(3)  # Allow new products to load

    except NoSuchElementException:
        print("No more 'Load More' button found — all products loaded.")
        break
    except ElementClickInterceptedException:
        print("Click intercepted — waiting and retrying...")
        time.sleep(2)

# Parse the fully loaded page
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
# <div class="ProductCard_productColorText__Slosp">Blue</div>
# Extract product titles
# Swiper_imageAspectConatiner__ELiyk loadingAnimation undefined
data = []
shoe_type_blocks = soup.find_all("div", class_="ProductCard_title__1OCu6 title")
product_description_blocks = soup.find_all("div", class_="ProductCard_description__saIH8 description")
actual_price_blocks = soup.find_all("span", class_ = "actual-price") 
price_blocks = soup.find_all("span", class_ = "price")
discount_blocks = soup.find_all("span", class_ = "discount")
shoe_color_blocks = soup.find_all("div", class_="ProductCard_productColorText__Slosp")
image_blocks = soup.find_all("div", class_="Swiper_imageAspectConatiner__ELiyk loadingAnimation undefined")

for shoe_type_block,product_description_block,actual_price_block,price_block,discount_block,shoe_color_block,image_block in zip(shoe_type_blocks,product_description_blocks,actual_price_blocks,price_blocks,discount_blocks,shoe_color_blocks,image_blocks):
    product_type = shoe_type_block.text.strip()
    product_description = product_description_block.get('title')
    actual_price = actual_price_block.find('span').text.strip()

    # logic to remove Rupee symbol from i tag of price
    i_tag = price_block.find('i')
    if i_tag:
        i_tag.decompose()  # Removes it from the tree

    # Now get the price text without the symbol
    # price = price_block.find('span').text.strip()
    price = price_block.get_text(strip=True)
    discount_offer = discount_block.text.strip()
    shoe_color = shoe_color_block.text.strip()
    image = image_block.find('img').get('src')
    print('Product Type : ',product_type)
    print('Product Description : ',product_description)
    print('Actual Price : ',actual_price)
    print('Price : ',price)
    print('Discount Offer : ',discount_offer)
    print('Shoe Color : ',shoe_color)
    print('Image : ',image)
    print("-" * 40)
    data.append({
        'Product Type': product_type,
        'Product Description': product_description,
        'Actual Price': actual_price,
        'Price': price,
        'Discount Offer': discount_offer,
        'Shoe Color': shoe_color,
        'Image': image
    })

# print("Total products found:", len(shoe_type_blocks))
df = pd.DataFrame(data)
df.to_csv('reebok_shoe_data.csv', index=False)