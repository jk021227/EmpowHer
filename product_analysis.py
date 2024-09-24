import pandas as pd
import matplotlib.pyplot as plt
import os

# function to load csv data based on user selection
def load_category_data():
    print("💕 Welcome to EmpowHer 💕\n")
    print("Select a category to see the Pink Tax information from Target.\n")
    print("Please choose a category:")
    # print("?. Shampoo")  # shampoo option commented out - I ran out of API calls...
    print("1. Razors")
    print("2. Deodorant")

    try:
        category_num = int(input("\nEnter the number of the category you want to explore: "))
        
        # determining file name based on user input
        if category_num == 1:
            file_name = 'razors_updated_file.csv'
            product_category = 'razors'
        elif category_num == 2:
            file_name = 'deodorant_updated_file.csv'
            product_category = 'deodorant'
        # uncomment this option once shampoo DB becomes available
        # elif category_num == 3:
        #     file_name = 'shampoo_updated_file.csv'
        #     product_category = 'shampoo'
        else:
            print("Invalid option, please choose a valid category number.")
            return None, None

        print(f"\n💅 Pink tax for {product_category} at Target:\n")
        return file_name, product_category

    except ValueError:
        print("Invalid input. Please enter a number.")
        return None, None

# function to convert price ranges to average price
def convert_price(price):
    if " - " in price:
        low, high = price.split(" - ")
        low = float(low.replace("$", ""))
        high = float(high.replace("$", ""))
        return round((low + high) / 2, 2)
    else:
        return float(price.replace("$", ""))

# main execution starts here:
file_name, product_category = load_category_data()  # getting file & category from user input

if file_name:  # checking if file_name is valid (user selected valid option)
    # loading csv data into df
    df = pd.read_csv(file_name)

    # applying convert_price() function to create a new column for average prices
    df['Average Price'] = df['Price'].apply(convert_price)

    # groupby 'is_girly' & calculate mean of average prices
    grouped = df.groupby('is_girly')['Average Price'].mean()

    # extracting average prices for girly & non-girly products
    girly_avg_price = grouped.get('yes', 0)
    non_girly_avg_price = grouped.get('no', 0)

    # calculating price difference
    price_difference = girly_avg_price - non_girly_avg_price

    # printing price difference for users
    if price_difference > 0:
        print(f"{product_category.capitalize()} products that are girly-coded are on average ~${price_difference:.2f} more expensive than those that are not.")
    elif price_difference < 0:
        print(f"{product_category.capitalize()} products that are not girly-coded are on average ~${-price_difference:.2f} more expensive than girly-coded ones.")
    else:
        print(f"There is no price difference between girly-coded and non-girly-coded {product_category} products.")

    # visualizing Pink Tax effect using a bar chart
    plt.figure(figsize=(7, 4))
    grouped.plot(kind='bar', color=['lightblue', 'pink'], legend=False)
    plt.title(f'Average Price of {product_category.capitalize()} Products by Gender Category (Pink Tax Effect)', fontsize=12)
    plt.ylabel('Average Price (USD)', fontsize=10)
    plt.xlabel('Gender Category', fontsize=10)
    plt.xticks(rotation=0)

    # adding a line to for extra visuals
    y1, y2 = grouped.values
    x1, x2 = 0, 1
    plt.plot([x1, x2], [y1, y2], color='red', linestyle='--')

    # adding annotation of price difference
    price_diff = y2 - y1
    plt.annotate(f'+${price_diff:.2f}', 
                 xy=(0.5, (y1 + y2) / 2),  # midpoint of line
                 xytext=(0, -15),  # 20 points below midpoint
                 textcoords='offset points', 
                 ha='center', va='top',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.show()

else:
    print("No valid category was selected.")
