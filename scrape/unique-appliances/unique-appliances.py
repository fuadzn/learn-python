import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import os
import time

# Shopify store - pakai JSON API untuk hasil yang lebih bersih & lengkap
BASE_URL = "https://uniqueappliances.com"
COLLECTION_HANDLE = "refrigerators-freezers"

# Headers ringan - tanpa Accept-Encoding agar tidak dapat response terenkripsi (br/gzip)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}


def clean_html(html_str):
    """Hapus tag HTML dari string deskripsi"""
    if not html_str:
        return ""
    return BeautifulSoup(html_str, 'html.parser').get_text(separator=' ', strip=True)


def fetch_products_page(collection_handle, page=1):
    """
    Ambil satu halaman produk dari Shopify JSON API.
    Shopify membatasi 250 produk per halaman.
    """
    url = f"{BASE_URL}/collections/{collection_handle}/products.json"
    params = {'limit': 250, 'page': page}
    response = requests.get(url, headers=HEADERS, params=params, timeout=15)
    response.raise_for_status()
    return response.json().get('products', [])


def fetch_all_products(collection_handle):
    """Ambil semua produk dari collection, handle pagination otomatis"""
    all_products = []
    page = 1

    while True:
        print(f"  Fetching page {page}...")
        products = fetch_products_page(collection_handle, page)

        if not products:
            break  # Tidak ada produk lagi

        all_products.extend(products)

        # Shopify max 250 per page; jika kurang dari 250, ini halaman terakhir
        if len(products) < 250:
            break

        page += 1
        time.sleep(0.5)  # Jeda kecil agar tidak diblokir

    return all_products


def parse_product(raw):
    """
    Ubah data mentah dari Shopify API menjadi format yang bersih.
    Setiap varian dianggap sebagai produk tersendiri (misal: warna berbeda).
    """
    products = []

    base_name = raw.get('title', 'Unknown')
    description = clean_html(raw.get('body_html', ''))
    product_type = raw.get('product_type', '')
    vendor = raw.get('vendor', '')
    tags = raw.get('tags', [])

    # Ambil semua gambar dan buat dictionary image per variant_id
    images = raw.get('images', [])
    # Gambar pertama sebagai default
    default_image = images[0]['src'] if images else None
    # Map variant_id -> src
    variant_image_map = {}
    for img in images:
        for vid in img.get('variant_ids', []):
            if vid not in variant_image_map:
                variant_image_map[vid] = img['src']

    variants = raw.get('variants', [])
    handle = raw.get('handle', '')
    product_url = f"{BASE_URL}/collections/{COLLECTION_HANDLE}/products/{handle}"

    for variant in variants:
        variant_id = variant.get('id')
        variant_title = variant.get('title', '')

        # Nama: gabungkan nama produk dan nama varian (kecuali "Default Title")
        if variant_title and variant_title != 'Default Title':
            name = f"{base_name} - {variant_title}"
        else:
            name = base_name

        # Harga dalam CAD
        price_raw = variant.get('price', '0')
        try:
            price = f"CA${float(price_raw):,.2f}"
        except (ValueError, TypeError):
            price = f"CA${price_raw}"

        # Harga compare (original sebelum diskon)
        compare_price_raw = variant.get('compare_at_price')
        if compare_price_raw:
            try:
                compare_price = f"CA${float(compare_price_raw):,.2f}"
            except (ValueError, TypeError):
                compare_price = f"CA${compare_price_raw}"
        else:
            compare_price = None

        # Gambar: cari gambar spesifik varian, fallback ke gambar pertama
        image_url = variant_image_map.get(variant_id, default_image)

        # Ketersediaan
        available = variant.get('available', False)

        products.append({
            'name': name,
            'sku': variant.get('sku', ''),
            'price': price,
            'compare_at_price': compare_price,
            'available': available,
            'description': description,
            'product_type': product_type,
            'vendor': vendor,
            'tags': tags,
            'image_url': image_url,
            'url': product_url,
        })

    return products


def main():
    print(f"Starting to scrape {BASE_URL}/collections/{COLLECTION_HANDLE}...")
    print("Using Shopify JSON API (no HTML parsing needed)\n")

    # Ambil semua produk dari API
    raw_products = fetch_all_products(COLLECTION_HANDLE)
    print(f"\nFound {len(raw_products)} product listings from API")

    # Parse setiap produk
    scraped_data = []
    for raw in raw_products:
        parsed = parse_product(raw)
        scraped_data.extend(parsed)

    print(f"Total variants/SKUs: {len(scraped_data)}")

    # Simpan ke JSON
    if not os.path.exists('output'):
        os.makedirs('output')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'output/unique_appliances_{timestamp}.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, ensure_ascii=False, indent=4)

    print(f"\n✓ Saved {len(scraped_data)} products to {filename}")

    # Tampilkan beberapa contoh
    print("\nSample output (first 3 products):")
    for p in scraped_data[:3]:
        print(f"  - {p['name']} | {p['price']} | img: {'✓' if p['image_url'] else '✗'}")


if __name__ == "__main__":
    main()