import pdb
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import re
import time
import pandas as pd

# URL target
BASE_URL = "https://futurofuturo.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def scrape_product_details(product_url):
    try:
        response = requests.get(product_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        product = {}

        # Product Name
        h2 = soup.find('h2')
        if h2:
            product['name'] = h2.get_text(strip=True)
        else:
            title_tag = soup.find('title')
            raw_title = title_tag.get_text(strip=True) if title_tag else 'Unknown'
            product['name'] = re.sub(r'\s*[-–]\s*White Dove.*$', '', raw_title).strip()

        # Price
        price_tag = soup.find('span', class_='sale-price-wrap')
        if price_tag:
            price_tag = price_tag.find('span')
            if price_tag:
                product['price'] = price_tag.get_text(strip=True)
        else:
            body_text = soup.get_text()
            price_match = re.search(r'Sale Price:\s*\$?([\d,]+\.?\d*)', body_text)
            product['price'] = f"${price_match.group(1)}" if price_match else 'N/A'

        # Description
        tab_description = soup.find('div', class_='description-tab')
        if tab_description:
            product['description'] = tab_description.get_text(strip=True)
        else:
            product['description'] = "No description"

        # Short Description
        short_description = soup.find('div', class_='specifications-tab')
        if short_description:
            short_description_p = short_description.find('p').get_text(strip=True)
            product['short_description'] = short_description_p
        else:
            product['short_description'] = "No short description"

        # Link
        product['url'] = product_url

        # Image
        image_tag = soup.find('meta', {'property': 'og:image'})
        if image_tag and image_tag.get('content'):
            product['image_url'] = image_tag['content'].strip()
        else:
            img_tag = soup.find('img', class_='wp-post-image')
            product['image_url'] = img_tag['src'] if img_tag and img_tag.get('src') else None

        print(f"  ✓ Scraped: {product['name']} — {product['price']} | img: {'✓' if product.get('image_url') else '✗'}")
        return product

    except Exception as e:
        print(f"  ✗ Error scraping {product_url}: {e}")
        return None


def get_product_links_from_collections(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        product_links = set()

        for item in soup.find_all('li'):
            if "data-product-id" in item.attrs:
                for a_tag in item.find_all('a', href=True):
                    href = a_tag['href']
                    
                    if re.search(r'futurofuturo\.com/', href):
                        product_links.add(href.rstrip('/') + '/')
                    elif re.match(r'^/product/[a-z0-9\-]+/?$', href):
                        product_links.add(f"{BASE_URL}{href.rstrip('/')}/")

                products = product_links

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

        product_links = get_product_links_from_collections(COLLECTIONS_URL)
        print(f"\nFound {len(product_links)} products total:")
        for link in product_links:
            print(f"  - {link}")
        print()

        all_products.extend(product_links)

    scraped_data = []
    for i, link in enumerate(all_products, 1):
        print(f"[{i}/{len(all_products)}] Scraping...")
        product_data = scrape_product_details(link)
        if product_data:
            scraped_data.append(product_data)
        if i < len(product_links):
            time.sleep(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_json = f'scrape/futuro-futuro/output/products_{timestamp}.json'
    filename_csv = f'scrape/futuro-futuro/output/products_{timestamp}.csv'
    
    with open(filename_json, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)
    
    with open(filename_csv, 'w', encoding='utf-8') as f:
        df = pd.DataFrame(scraped_data)
        df.to_csv(f, index=False)
    
    print(f"\n✓ Scraping completed! {len(scraped_data)} products saved to {filename_json} and {filename_csv}")

if __name__ == "__main__":
    main()