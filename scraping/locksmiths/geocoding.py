import pandas as pd
from geopy.geocoders import Nominatim
import time

# Read CSV and filter for unknown cities
new_df = pd.read_csv("cleaned_locksmiths.csv")

# Proxy settings
proxy = {
    "http": "http://25f962c67d67a9a10edc:358a70d297fbc821@gw.dataimpulse.com:823",
    "https": "http://25f962c67d67a9a10edc:358a70d297fbc821@gw.dataimpulse.com:823",
}

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapi", proxies=proxy, timeout=10)

# Function to clean and simplify address
def simplify_address(address):
    if not isinstance(address, str):
        return []
    address_parts = address.split(',')
    variations = []
    for i in range(len(address_parts)):
        simplified = ', '.join(address_parts[i:]).strip()
        if simplified:
            variations.append(simplified)
    return variations

# Function to geocode with retries
def geocode_with_retries(raw_address):
    address_variations = simplify_address(raw_address)
    for addr in address_variations:
        try:
            print(f"Trying: {addr}")
            result = geolocator.geocode(addr)
            time.sleep(1)  # Avoid rate limits
            if result and "United States" in result.address:
                print(f"Found: {result.address}")
                return result
        except Exception as e:
            print(f"Error geocoding {addr}: {e}")
            continue
    return None

# Function to process each row
def process_row(row):
    raw_address = row["Location"]  # Keep the original address
    if raw_address:
        result = geocode_with_retries(raw_address)
        if result:
            new_address = result.address  # Geocoded address
            row["Full Address"] = new_address  # Store new address in a separate column
        else:
            row["Full Address"] = raw_address  # Retain raw address if geocoding fails
            print(f"No valid location found, keeping raw: {raw_address}")
    else:
        row["Full Address"] = "Invalid or empty address"  # Handle empty addresses
        print("Invalid or empty address.")
    return row

# Apply the processing function to each row
updated_df = new_df.apply(process_row, axis=1)

# Save updated DataFrame to a new CSV file
updated_df.to_csv("updated_locksmiths.csv", index=False)

print("Updated locksmiths data saved to 'updated_locksmiths.csv'.")
