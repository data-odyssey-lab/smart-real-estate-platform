import re
from database.location_normalizer import get_constituency

def clean_price(price_str):
    if not price_str or price_str == 'N/A':
        return None
    digits = re.sub(r'[^\d.]', '', price_str)
    if not digits:
        return None
    value = int(digits)
    # clean unrealistic prizes
    if value < 500000:
        return None
    return value

def clean_numeric(value_str):
    if not value_str or value_str == 'N/A':
        return None
    digits = re.sub(r'[^\d.]', '', value_str)
    return float(digits) if digits else None

def clean_floor_size(value_str):
    if not value_str or value_str == 'N/A':
        return None
    digits = re.sub(r'[^\d.]', '', value_str)
    if not digits:
        return None
    value = float(digits)
    # flag unrealistic values as None
    if value < 10 or value > 2000:
        return None
    return value

def clean_listing(listing):
    price = clean_price(listing.get('price'))
    floor_size = clean_floor_size(listing.get('floor_size'))
    return {
        'title': listing.get('title'),
        'price_raw': listing.get('price'),
        'price': price,
        'price_flag': 'outlier' if price is None and listing.get('price') else None,
        'location': listing.get('location'),
        'constituency': get_constituency(listing.get('location')),
        'address': listing.get('address'),
        'bedrooms': clean_numeric(listing.get('bedrooms')),
        'bathrooms': clean_numeric(listing.get('bathrooms')),
        'floor_size_raw': listing.get('floor_size'),
        'floor_size': floor_size,
        'floor_size_flag': 'outlier' if floor_size is None and listing.get('floor_size') else None,
        'excerpt': listing.get('excerpt'),
        'link': listing.get('link'),
    }

def clean_listings(listings):
    return [clean_listing(i) for i in listings]
