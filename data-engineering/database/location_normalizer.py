LOCATION_TO_CONSTITUENCY = {
    "Westlands": "Westlands",
    "Kileleshwa": "Langata",
    "Kilimani": "Langata",
    "Riverside": "Westlands",
    "Lavington": "Langata",
    "Karen": "Langata",
    "Runda": "Westlands",
    "Spring Valley": "Westlands",
    "Kiambu Road": "Westlands",
    "Loresho": "Westlands",
    "Lower Kabete": "Westlands",
    "Syokimau": "Mavoko",
    "Parklands": "Westlands",
    "Kerarapon": "Langata",
    "Peponi": "Westlands",
    "Gigiri": "Westlands",
    "Industrial Area": "Makadara",
    "Kitisuru": "Westlands",
    "Thigiri": "Westlands",
    "Garden Estate": "Roysambu",
    "Joska": "Embakasi East",
    "Katani": "Mavoko",
    "Mlolongo": "Mlolongo",
    "Mombasa Rd": "Embakasi East",
    "Muthangari": "Westlands",
    "Ridgeways": "Roysambu",
    "Githurai": "Roysambu",
    "Kyuna": "Westlands",
    "Langata": "Langata",
    "Mountain View": "Westlands",
    "Rosslyn": "Westlands",
}

def get_constituency(location):
    if not location or location == "N/A":
        return None
    return LOCATION_TO_CONSTITUENCY.get(location.strip(), "Unknown")