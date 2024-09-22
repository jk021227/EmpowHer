from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from dotenv import load_dotenv
import time
import pandas as pd


# Load environment variables from .env file
load_dotenv()

# Set up Selenium WebDriver using SafariDriver
def setup_safari():
    print("Setting up Selenium WebDriver for Safari...")
    driver = webdriver.Safari()  # No need for a service or path with Safari
    return driver

# Function to scroll down the page to load more products (if lazy loading is used)
def scroll_down(driver):
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(13):  # Scroll 13 times (adjust if needed)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Wait a bit for more products to load

# Function to scrape product details using Selenium with fallback for missing elements
def scrape_products_selenium(driver):
    # Find product cards using a more reliable wrapper selector
    product_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

    # Print the number of product cards found
    print(f"Found {len(product_cards)} product cards.")

    products = []

    for card in product_cards:
        try:
            # Extract product image URL
            try:
                image_tag = card.find_element(By.CSS_SELECTOR, 'img')
                image_url = image_tag.get_attribute('src') if image_tag else 'No Image'
            except NoSuchElementException:
                image_url = 'No Image'

            # Extract product name
            try:
                product_name_tag = card.find_element(By.CSS_SELECTOR, 'a[data-test="product-title"]')
                product_name = product_name_tag.text.strip() if product_name_tag else 'No Product Name'
            except NoSuchElementException:
                product_name = 'No Product Name'

            # Extract brand name
            try:
                brand_tag = card.find_element(By.CSS_SELECTOR, 'a[data-test="@web/ProductCard/ProductCardBrandAndRibbonMessage/brand"]')
                brand_name = brand_tag.text.strip() if brand_tag else 'No Brand'
            except NoSuchElementException:
                brand_name = 'No Brand'

            # Extract price
            try:
                price_tag = card.find_element(By.CSS_SELECTOR, 'span[data-test="current-price"]')
                price = price_tag.text.strip() if price_tag else 'No Price'
            except NoSuchElementException:
                price = 'No Price'

            # Append the product information to the products list
            products.append({
                'Product Name': product_name,
                'Brand': brand_name,
                'Price': price,
                'Image URL': image_url
            })
        except StaleElementReferenceException:
            print("Stale element encountered, moving to the next item.")

    return products

# Function to handle pagination and scrape all products
def scrape_all_pages(category_num):
    driver = setup_safari()

    # Define category based on user selection
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
        # Scroll down to load more products (for lazy-loaded pages)
        scroll_down(driver)

        # Scrape the products from the current page
        products = scrape_products_selenium(driver)
        all_products.extend(products)

        # Try to find and click the "Next Page" button using JavaScript
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test="next"]')
            
            # Check if the button is disabled
            if next_button.get_attribute('disabled'):
                print("Reached the last page. No more pages to load.")
                break

            # Scroll to the button and click it
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)  # Click using JavaScript
            time.sleep(2)  # Wait for the next page to load
            
        except (NoSuchElementException, ElementClickInterceptedException):
            print("No more pages to load or unable to click the next button.")
            break


    driver.quit()  # Close the browser once done
    return all_products

# Function to save products to a CSV file and print the DataFrame
def save_and_print_products(category_num: int) -> None:
    # Scrape products across all pages using Selenium
    products = scrape_all_pages(category_num)

    if not products:
        print("No products found.")
        return

    # Create a DataFrame from the products list
    df = pd.DataFrame(products)

    # Print the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    category = 'shampoo' if category_num == 1 else 'razors' if category_num == 2 else 'deodorant'
    csv_filename = f"{category}_products.csv"
    df.to_csv(csv_filename, index=False)

    print(f"Products saved to {csv_filename}")

# Uncomment the code below to scrap new databases!

# # Main function to guide the user through the category selection and scraping process
# def main():
#     print("💕 Welcome to Pink Tax 101 💕\n")
#     print("Have you ever heard about the 'Pink Tax'? 🤔")
#     print("It's that sneaky little extra charge applied to products marketed toward women, even though similar products for men often cost less. 😠")
#     print("Let's dive in and explore how much more women pay for basic items like razors, shampoo, and deodorant.")
#     print("You get to pick a category, and we'll show you just how real the Pink Tax is! 💸")
#     print("Ready to see the price differences? Let's go! 🚀\n")

#     while True:
#         print("Pick a category:")
#         print("1. Shampoo")
#         print("2. Razors")
#         print("3. Deodorant")
#         try:
#             category_num = int(input("\nEnter the number of the category you want to explore: "))
#             if category_num in [1, 2, 3]:
#                 # Call the save_and_print_products function with the valid category number
#                 save_and_print_products(category_num)
#                 break  # Exit the loop after successfully calling the function
#             else:
#                 print("Invalid category number. Please choose an existing number.😔 \n")
#         except ValueError:
#             print("Invalid input. Please enter a number.🥹\n")

# # Start the program
# if __name__ == "__main__":
#     main()
