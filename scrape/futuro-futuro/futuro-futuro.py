from ast import main
import requests
from bs4 import BeautifulSoup
# import pandas as pd
import json
# import os
from datetime import datetime
# import time

# URL target
BASE_URL = "https://futurofuturo.com"

# User-Agent headers agar tidak diblokir
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def get_product_description(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # product_links = set()
        products = []

        for item in soup.find_all('li'):
            if "data-product-id" in item.attrs:
                h2 = item.find('h2', class_='woocommerce-loop-product__title')
                name = h2.get_text(strip=True) if h2 else (item.find('h2').get_text(strip=True) if item.find('h2') else 'N/A')
                description = item.find('div', class_='text').get_text(strip=True)
                price = item.find('span', class_='green').get_text(strip=True)
                sku = item.find('div', class_='sku').get_text(strip=True)
                product = {
                    'name': name,
                    'description': description,
                    'price': price,
                    'sku': sku,
                    'product_id': item.get('data-product-id'),
                }
                products.append(product)
                print(f"  ✓ Scraped: {product['name']} (ID: {product['product_id']})")
                
                
        # Get all data from first page <li> tag
        # for item in soup.find_all('li', class_='post-'):
            # Get all data from <p> tag
            # for p in item.find_all('p', class_=''):
            #     product_links.add(p.get_text())

        return products

    except Exception as e:
        print(f"Error fetching collections page: {e}")
        return []


def main():
    type = [
        'island-range-hoods',
        'wall-range-hoods',
        'built-in-range-hoods',
        'downdraft-induction-cooktop',
        'range-hood-accessories'
    ]

    all_products = []

    for t in type:
        COLLECTIONS_URL = f"{BASE_URL}/{t}"
        print(f"Starting to scrape {COLLECTIONS_URL}...")

        # Ambil daftar link produk dari halaman collections
        products = get_product_description(COLLECTIONS_URL)
        all_products.extend(products)

    print(f"\nFound {len(all_products)} products total:")
    for link in all_products:
        print(f"  - {link}")
    print()

    # save json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'scrape/futuro-futuro/output/futurofuturo_{timestamp}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)

            
    print(f"\n✓ Scraping completed! {len(all_products)} products saved to {filename}")

if __name__ == "__main__":
    main()