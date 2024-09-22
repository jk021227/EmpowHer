import pandas as pd
import matplotlib.pyplot as plt
import os

print("💅 So Pink tax for {razors} at Target are...:")

# Load the CSV data
file_name = 'razors_updated_file.csv'  # You can also make this variable dynamic if needed
product_category = os.path.basename(file_name).split('_')[0]  # Extracting the category like 'razors'
print(f"💅 So Pink tax for {product_category} at Target are...:")

df = pd.read_csv(file_name)


# Define the function to convert price ranges to average price
def convert_price(price):
    if " - " in price:
        low, high = price.split(" - ")
        low = float(low.replace("$", ""))
        high = float(high.replace("$", ""))
        return round((low + high) / 2, 2)
    else:
        return float(price.replace("$", ""))

# Apply the function to create a new column for average prices
df['Average Price'] = df['Price'].apply(convert_price)

# Drop the 'Price' and 'Image URL' columns
avg_df = df.drop(columns=['Price', 'Image URL'])

# Group by 'is_girly' and calculate the mean average price
grouped = avg_df.groupby('is_girly')['Average Price'].mean()

# Extract the average prices for girly and non-girly products
girly_avg_price = grouped.get('yes', 0)
non_girly_avg_price = grouped.get('no', 0)

# Calculate the price difference
price_difference = girly_avg_price - non_girly_avg_price

# Print a clear statement
if price_difference > 0:
    print(f"Razors that are girly-coded are on average ~${price_difference:.2f} more expensive than those that are not.")
elif price_difference < 0:
    print(f"Razors that are not girly-coded are on average ~${-price_difference:.2f} more expensive than girly-coded ones.")
else:
    print("There is no price difference between girly-coded and non-girly-coded razors.")

# Visualize the Pink Tax effect using a bar chart
plt.figure(figsize=(7, 4))
grouped.plot(kind='bar', color=['lightblue', 'pink'], legend=False)
plt.title('Average Price of Razor Products by Gender Category (Pink Tax Effect)', fontsize=12)
plt.ylabel('Average Price (USD)', fontsize=10)
plt.xlabel('Gender Category', fontsize=10)
plt.xticks(rotation=0)

# Add a line to show the price increase
y1, y2 = grouped.values
x1, x2 = 0, 1
plt.plot([x1, x2], [y1, y2], color='red', linestyle='--')

# Add an annotation for the price difference
price_diff = y2 - y1
plt.annotate(f'+${price_diff:.2f}', 
             xy=(0.5, (y1 + y2) / 2),  # midpoint of the line
             xytext=(0, -15),  # 20 points below the midpoint
             textcoords='offset points', 
             ha='center', va='top',
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
plt.tight_layout()

# Show the plot
plt.show()