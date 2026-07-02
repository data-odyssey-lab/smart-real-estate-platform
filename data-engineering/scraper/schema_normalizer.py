UNIFIED_LISTING_FIELDS = {
    'source': None,
    'title': None,
    'price': None,
    'location': None,
    'bedrooms': None,
    'bathrooms': None,
    'floor_size': None,
    'excerpt': None,
    'address': None,
    'link': None,
}

def normalize_schema(listing):
    normalized_listing = UNIFIED_LISTING_FIELDS.copy()
    normalized_listing.update(listing)

    return normalized_listing

