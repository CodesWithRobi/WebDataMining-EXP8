import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

def convert_price_to_float(price):
    # Remove currency symbols and commas, and then convert to float
    price = re.sub(r'[^\d.]', '', price)  # Remove non-digit characters except '.'
    return float(price) if price else 0.0

def get_shopclues_products(search_query):
    base_url = 'https://www.shopclues.com'
    # headers = {
    #     'User-Agent': 'Your User Agent'  # Add your User Agent here
    # }

    search_query = search_query.replace(' ', '+')
    url = f'{base_url}/search?q={search_query}'

    response = requests.get(url)
    products_data = []  # List to store product information

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'class': 'column col3 search_blocks'})
        for product in products:
            title = product.find('h2').text.strip()
            price = product.find('span', {'class': 'p_price'}).text.strip()[1:]
            

            products_data.append({'Product': title, 'Price': price})
        

    return sorted(products_data, key=lambda x: convert_price_to_float(x['Price']))

search_query = input('Enter product to search on ShopClues: ')
products = get_shopclues_products(search_query)

# Displaying product data using a bar chart
if products:  # Check if products list is not empty
    product_names = [product['Product'][:30] if len(product['Product']) > 30 else product['Product'] for product in products]
    product_prices = [convert_price_to_float(product['Price']) for product in products]

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(product_prices)), product_prices, color='skyblue')
    plt.xlabel('Price')
    plt.ylabel('Product')
    plt.title(f'Products and their Prices on shopclues for {search_query.capitalize()} (Ascending Order)')
    plt.yticks(range(len(product_prices)), product_names)  # Setting y-axis labels as shortened product names
    plt.tight_layout()
    plt.show()
else:
    print('No products found.')
