from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Set up Selenium with Chrome
driver = webdriver.Chrome()  # Make sure chromedriver is installed

# Open the page
driver.get("https://reebok.abfrl.in/c/men-sale-footwear")

# Wait for JS to load (increase if needed)
time.sleep(5)

# Scroll to the bottom repeatedly to load all products
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new products to load
    time.sleep(3)

    # Calculate new scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    # If height hasn't changed, all products are loaded
    if new_height == last_height:
        break
    last_height = new_height

# Get page source after JS execution
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()

shoe_type_blocks = soup.find_all('div', class_='ProductCard_title__1OCu6 title')

for block in shoe_type_blocks:
    print(block.text.strip())

print('Total products:', len(shoe_type_blocks))
print('end')
# for block in shoe_type_blocks:
#     shoe_type = block.text.strip()
#     print("Shoe Type:", shoe_type)
#     print("-" * 40)

# print('end')
# product_list = soup.find_all('div', class_='grid-product__secondary-image small--hide lazyloaded')

# product_list = soup.find_all('div', class_='grid-product__price')

# print(product_list[0])

# original_price_tag = soup.find('span', class_='grid-product__price--original')
# original_price = original_price_tag.find('span', class_='money').text.strip() if original_price_tag else None

# # Extract sale price (second occurrence of <span class="money">)
# all_money_spans = soup.find_all('span', class_='money')
# sale_price = all_money_spans[1].text.strip() if len(all_money_spans) > 1 else None

# # Extract savings
# savings_tag = soup.find('span', class_='grid-product__price--savings')
# savings = savings_tag.text.strip() if savings_tag else None

# print("Original Price:", original_price)
# print("Sale Price:", sale_price)
# print("Savings:", savings)


# Find all product price blocks
# price_blocks = soup.find_all('div', class_='grid-product__price')
# count = 0
# for block in price_blocks:
#     # Original Price
#     original_price_tag = block.find('span', class_='grid-product__price--original')
#     original_price = original_price_tag.find('span', class_='money').text.strip() if original_price_tag else None

#     # Sale Price (find all 'money' spans and get the second one if available)
#     money_spans = block.find_all('span', class_='money')
#     sale_price = None
#     if len(money_spans) == 2:
#         sale_price = money_spans[1].text.strip()
#     elif len(money_spans) == 1:
#         sale_price = money_spans[0].text.strip()

#     # Savings
#     savings_tag = block.find('span', class_='grid-product__price--savings')
#     savings = savings_tag.text.strip() if savings_tag else None
#     count += 1
#     print("Product Number:", count)
#     print("Original Price:", original_price)
#     print("Sale Price:", sale_price)
#     print("Savings:", savings)
#     print("-" * 40)