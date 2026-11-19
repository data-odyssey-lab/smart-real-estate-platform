import re
from urllib.parse import urlparse
from database.location_normalizer import get_constituency

def clean_price(price_str):
    """Clean and validates property price"""
    
    if not price_str or price_str == 'N/A':
        return None, None
    digits = re.sub(r'[^\d.]', '', price_str)
    if not digits:
        return None, 'invalid'
    value = int(digits)
    # clean unrealistic prizes
    if value < 500000:
        return None, 'outlier'
    return value, None

def clean_numeric(value_str):
    """Convert numeric to float"""

    if not value_str or value_str == 'N/A':
        return None
    digits = re.sub(r'[^\d.]', '', value_str)
    return float(digits) if digits else None

def clean_floor_size(value_str):
    """Clean and validates floor size"""
    
    if not value_str or value_str == 'N/A':
        return None, None
    digits = re.sub(r'[^\d.]', '', value_str)
    if not digits:
        return None, 'invalid'
    value = float(digits)
    # flag unrealistic values as None
    if value < 10 or value > 2000:
        return None, 'outlier'
    return value, None

import hashlib

def extract_source_listing_id(link):
    """Extracts the numeric listing ID from a property URL."""

    if not link or link == "N/A":
        return None
    path = urlparse(link).path.rstrip("/")
    match = re.search(r'-(\d+)$', path)
    return match.group(1) if match else None

def generate_content_hash(listing):
    """Generates a unique hash for a listing based on its key attributes"""

    key = (
        str(listing.get('title') or '') +
        str(listing.get('price_raw') or '') +
        str(listing.get('location') or '') +
        str(listing.get('bedrooms') or '') +
        str(listing.get('bathrooms') or '')
    )
    return hashlib.md5(key.encode("utf-8")).hexdigest()

def clean_listing(listing):
    """Cleans a single listing dictionary and returns a cleaned dictionary"""

    price, price_flag = clean_price(listing.get('price'))
    floor_size, floor_size_flag = clean_floor_size(listing.get('floor_size'))
    return {
        'title': listing.get('title'),
        'source': listing.get('source'),
        'price_raw': listing.get('price'),
        # 'price': price,
        # 'price_flag': price_flag,
        'region': listing.get('region'),
        'location': listing.get('location'),
        'constituency': get_constituency(listing.get('location')),
        'address': listing.get('address'),
        'bedrooms': clean_numeric(listing.get('bedrooms')),
        'bathrooms': clean_numeric(listing.get('bathrooms')),
        'floor_size_raw': listing.get('floor_size'),
        # 'floor_size': floor_size,
        # 'floor_size_flag': floor_size_flag,
        'excerpt': listing.get('excerpt'),
        'link': listing.get('link'),
        'source_listing_id': extract_source_listing_id(listing.get('link')),
        'content_hash': generate_content_hash(listing),
        'scraped_at': listing.get('scraped_at'),
    }

def clean_listings(listings):
    """Cleans multiple listings and returns a list of cleaned listings"""
    return [clean_listing(i) for i in listings]
