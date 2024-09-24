from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
import os

# setting up Selenium WebDriver using SafariDriver
def setup_safari():
    print("Setting up Selenium WebDriver for Safari...") # intialization comment for user
    driver = webdriver.Safari()
    return driver

# function to scroll down the page to load more products (if lazy loading is used)
def scroll_down(driver):
    time.sleep(1)  # waiting for page to load, without it the first 4ish products' image URL are not scrapped
    body = driver.find_element(By.TAG_NAME, 'body') # retrieving the body element
    for _ in range(13):  # scrolling 13 times (adjust if needed)
        body.send_keys(Keys.PAGE_DOWN) # imitating PAGE_DOWN key press
        time.sleep(1)  # waiting a bit for more products to load

# function to scrape product details using Selenium
def scrape_products_selenium(driver):
    # finding product cards
    product_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    # debugging: printing number of product cards found
    # print(f"Found {len(product_cards)} product cards.")

    products = []

    for card in product_cards:
        try:
            # extracting product image URL
            try:
                image_tag = card.find_element(By.CSS_SELECTOR, 'img')
                image_url = image_tag.get_attribute('src') if image_tag else 'No Image'
            except NoSuchElementException:
                image_url = 'No Image'

            # extracting product name
            try:
                product_name_tag = card.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')
                product_name = product_name_tag.text.strip() if product_name_tag else 'No Product Name'
            except NoSuchElementException:
                product_name = 'No Product Name'

            # extracting brand name
            try:
                brand_tag = card.find_element(By.CSS_SELECTOR, 'a[data-test="@web/ProductCard/ProductCardBrandAndRibbonMessage/brand"]')
                brand_name = brand_tag.text.strip() if brand_tag else 'No Brand'
            except NoSuchElementException:
                brand_name = 'No Brand'

            # extracting price
            try:
                price_tag = card.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')
                price = price_tag.text.strip() if price_tag else 'No Price'
            except NoSuchElementException:
                price = 'No Price'

            # appending product information to products list
            products.append({
                'Product Name': product_name,
                'Brand': brand_name,
                'Price': price,
                'Image URL': image_url
            })
        except StaleElementReferenceException:
            print("Stale element encountered, moving to the next item.")

    return products

# function to handle pagination (multiple product pages) & scrape all products
def scrape_all_pages(category_num):
    driver = setup_safari()

    # defining category based on user selection
    if category_num == 1:
        category = "shampoo"
    elif category_num == 2:
        category = "razors"
    elif category_num == 3:
        category = "deodorant"

    search_url = f"https://www.target.com/s?searchTerm={category}&tref=typeahead%7Cterm%7C{category}%7C%7C%7Chistory"
    
    driver.get(search_url)

    all_products = []

    while True:
        # scrolling down to load more products (for lazy-loaded pages - seems to time out if not scrolled)
        scroll_down(driver)

        # scraping products from current page
        products = scrape_products_selenium(driver)
        # print(products[0]) - commented out for debugging
        all_products.extend(products)

        # clicking "Next Page" button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')
            
            # checking if the button is disabled (last page)
            if next_button.get_attribute('disabled'):
                print("Reached the last page. No more pages to load.")
                break

            # scrolling to button & click it
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button) # execute_script enables JavaScript code 
            driver.execute_script("arguments[0].click();", next_button)  # JavaScript function to click the button
            time.sleep(2)  # waiting for next page to load
            
        except (NoSuchElementException, ElementClickInterceptedException):
            print("No more pages to load or unable to click the next button.")
            break


    driver.quit()  # closing browser once done
    return all_products

# function to save products to a csv file & print df
def save_to_csv(category_num: int) -> None:
    # scraping products across all pages
    products = scrape_all_pages(category_num)

    if not products:
        print("No products found.")
        return

    # creating df from products list
    df = pd.DataFrame(products)

    # debugging - printing the DataFrame
    # print(df)

    # saving df to csv file
    os.makedirs('./csv_files', exist_ok=True)
    category = 'shampoo' if category_num == 1 else 'razors' if category_num == 2 else 'deodorant'
    csv_filename = f"./csv_files/{category}_products.csv"
    df.to_csv(csv_filename, index=False)

    print(f"Products saved to {csv_filename}")

# Uncomment the code below to scrap new databases!

# main function for user interaction
def main():
    print("💕 Welcome to Pink Tax 101 💕\n")
    print("Have you ever heard about the 'Pink Tax'? 🤔")
    print("It's that sneaky little extra charge applied to products marketed toward women, even though similar products for men often cost less. 😠")
    print("Let's dive in and explore how much more women pay for basic items like razors, shampoo, and deodorant.")
    print("You get to pick a category, and we'll show you just how real the Pink Tax is! 💸")
    print("Ready to see the price differences? Let's go! 🚀\n")

    while True:
        print("Pick a category:")
        print("1. Shampoo")
        print("2. Razors")
        print("3. Deodorant")
        try:
            category_num = int(input("\nEnter the number of the category you want to explore: "))
            if category_num in [1, 2, 3]:
                # calling  save_to_csv() with valid category number
                save_to_csv(category_num)
                break  # exiting loop after successfully calling function
            else:
                print("Invalid category number. Please choose an existing number.😔 \n")
        except ValueError:
            print("Invalid input. Please enter a number.🥹\n")

if __name__ == "__main__":
    main()
