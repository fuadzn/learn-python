import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import re
import time

# URL target
BASE_URL = "https://whitedoveusa.com"
COLLECTIONS_URL = f"{BASE_URL}/collections"

# User-Agent headers agar tidak diblokir
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def scrape_product_details(product_url):
    """Scrape detail dari halaman produk individual (WordPress/WooCommerce)"""
    try:
        response = requests.get(product_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        product = {}

        # Nama Produk - ambil dari <h1> atau <title>
        h1 = soup.find('h1')
        if h1:
            product['name'] = h1.get_text(strip=True)
        else:
            title_tag = soup.find('title')
            raw_title = title_tag.get_text(strip=True) if title_tag else 'Unknown'
            # Hapus " - White Dove" dari judul
            product['name'] = re.sub(r'\s*[-–]\s*White Dove.*$', '', raw_title).strip()

        # Harga - WooCommerce pakai class "woocommerce-Price-amount"
        price_tag = soup.find('span', class_='woocommerce-Price-amount')
        if price_tag:
            product['price'] = price_tag.get_text(strip=True)
        else:
            # Cari teks harga dari pattern "Starting at $X"
            body_text = soup.get_text()
            price_match = re.search(r'Starting at\s*\$?([\d,]+\.?\d*)', body_text)
            product['price'] = f"${price_match.group(1)}" if price_match else 'N/A'

        # Deskripsi - meta description (paling reliable untuk site ini)
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            product['description'] = meta_desc['content'].strip()
        else:
            # Coba dari OG description
            og_desc = soup.find('meta', {'property': 'og:description'})
            product['description'] = og_desc['content'].strip() if og_desc and og_desc.get('content') else 'No description'

        # Koleksi / Kategori
        breadcrumb = soup.find('nav', class_='woocommerce-breadcrumb')
        if breadcrumb:
            product['category'] = breadcrumb.get_text(separator=' > ', strip=True)
        else:
            product['category'] = 'Mattresses'

        # Fitur utama produk (bullet points)
        features = []
        entry_content = soup.find('div', class_='entry-content') or soup.find('div', class_='product-description')
        if entry_content:
            for li in entry_content.find_all('li')[:10]:
                text = li.get_text(strip=True)
                if text:
                    features.append(text)
        product['features'] = features

        # URL
        # Gambar Produk - ambil dari og:image (paling reliable)
        og_image = soup.find('meta', {'property': 'og:image'})
        if og_image and og_image.get('content'):
            product['image_url'] = og_image['content'].strip()
        else:
            # Fallback: WooCommerce product gallery main image
            img_tag = soup.find('img', class_='wp-post-image')
            product['image_url'] = img_tag['src'] if img_tag and img_tag.get('src') else None

        product['url'] = product_url

        print(f"  ✓ Scraped: {product['name']} — {product['price']} | img: {'✓' if product.get('image_url') else '✗'}")
        return product

    except Exception as e:
        print(f"  ✗ Error scraping {product_url}: {e}")
        return None


def get_product_links_from_collections(url):
    """
    Ambil semua link produk dari halaman collections.
    Site ini adalah WordPress/WooCommerce, bukan Shopify.
    Product URL pattern: https://whitedoveusa.com/product/<slug>/
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        product_links = set()

        # Cari semua <a> tag yang href-nya mengandung /product/
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Match pola: https://whitedoveusa.com/product/<slug>/
            if re.search(r'whitedoveusa\.com/product/[a-z0-9\-]+/?$', href):
                product_links.add(href.rstrip('/') + '/')
            elif re.match(r'^/product/[a-z0-9\-]+/?$', href):
                product_links.add(f"{BASE_URL}{href.rstrip('/')}/")

        return sorted(product_links)

    except Exception as e:
        print(f"Error fetching collections page: {e}")
        return []


def main():
    print(f"Starting to scrape {COLLECTIONS_URL}...\n")

    # Ambil daftar link produk dari halaman collections
    product_links = get_product_links_from_collections(COLLECTIONS_URL)

    print(f"Found {len(product_links)} products:")
    for link in product_links:
        print(f"  - {link}")
    print()

    if not product_links:
        print("No product links found. Check the URL or site structure.")
        return

    # Scrape detail setiap produk
    scraped_data = []
    for i, link in enumerate(product_links, 1):
        print(f"[{i}/{len(product_links)}] Scraping...")
        product_data = scrape_product_details(link)
        if product_data:
            scraped_data.append(product_data)
        # Jeda antar request agar tidak diblokir
        if i < len(product_links):
            time.sleep(1)

    # Simpan ke file JSON
    if not os.path.exists('output'):
        os.makedirs('output')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'output/whitedove_{timestamp}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)

    print(f"\n✓ Scraping completed! {len(scraped_data)} products saved to {filename}")


if __name__ == "__main__":
    main()