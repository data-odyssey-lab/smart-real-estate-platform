import re
from database.location_normalizer import get_constituency

def clean_price(price_str):
    if not price_str or price_str == 'N/A':
        return None
    digits = re.sub(r'[^\d.]', '', price_str)
    return int(digits) if digits else None

def clean_numeric(value_str):
    if not value_str or value_str == 'N/A':
        return None
    digits = re.sub(r'[^\d.]', '', value_str)
    return float(digits) if digits else None

def clean_listing(listing):
    return {
        'title': listing.get('title'),
        'price_raw': listing.get('price'),
        'price': clean_price(listing.get('price')),
        'location': listing.get('location'),
        'constituency': get_constituency(listing.get('location')),
        'address': listing.get('address'),
        'bedrooms': clean_numeric(listing.get('bedrooms')),
        'bathrooms': clean_numeric(listing.get('bathrooms')),
        'floor_size_raw': listing.get('floor_size'),
        'floor_size': clean_numeric(listing.get('floor_size')),
        'excerpt': listing.get('excerpt'),
        'link': listing.get('link'),
    }

def clean_listings(listings):
    return [clean_listing(i) for i in listings]
