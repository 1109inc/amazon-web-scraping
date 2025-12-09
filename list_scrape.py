from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import random
# --- START: Browser options (user-agent and automation flags) ---
options = Options()

# Set a common desktop User-Agent so requests look like a normal browser.
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
options.add_argument(f"user-agent={USER_AGENT}")

# Disable some Chrome automation flags to reduce visible automation traces.
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# --- END: Browser options ---

# Initialize the Chrome driver with the configured options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the search results URL to scrape (change this for different queries)
URL = 'https://www.amazon.in/s?k=phones&crid=1EHWVAQAUL4UB&sprefix=phone%2Caps%2C215&ref=nb_sb_noss_2'

# Open the page
driver.get(URL)

# Add a short, random pause to mimic human browsing
time.sleep(random.uniform(3, 7))

# Wait for dynamic content: block until at least one product list item appears
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listitem']"))
    )
except Exception:
    print("Timed out waiting for search results list to load.")
    # Script will continue, but results may be incomplete or empty.

# Capture the rendered HTML after the page has loaded
html_content = driver.page_source

# Close the browser now that we have the HTML
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find product containers (each product on the results page)
big_div = soup.find_all('div', role='listitem')

# For debugging: uncomment to inspect the structure of the first item
# print(big_div[0])

# Initialize a list to store scraped product data
product_data_list = []
print(f"Found {len(big_div)} potential product items.")

for i,div in enumerate(big_div):
    # Locate the product anchor by its class and build the full product URL
    link_tag = div.find('a', class_='a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal')
    product_url = ("https://www.amazon.in" + link_tag.get('href')) if link_tag else "N/A"

    # The product title is usually inside an <h2> within the anchor
    h2_tag = link_tag.find('h2') if link_tag else None

    # Extract the visible title text from the span inside the H2
    title = h2_tag.span.text.strip() if h2_tag and h2_tag.span else None
    star_rating=div.find('span', class_='a-icon-alt')
    currency=div.find('span', class_='a-price-symbol')
    price=div.find('span', class_='a-price-whole')
    reviews=div.find('span', class_="a-size-mini puis-normal-weight-text s-underline-text")
    full_price = f"{currency.text.strip()}{price.text.strip()}" if currency and price else "N/A"
    
    if title:
        # Print extracted details for verification
        print(f"   ✅ Title: {title}")
        print(f"   🔗 URL: {product_url}")
        print(f"   ⭐ Rating: {star_rating.text.strip() if star_rating else 'N/A'}")
        print(f"   💰 Price: {full_price}")
        print(f"   📝 Reviews: {reviews.text.strip() if reviews else 'N/A'}")
        data = {
            'ID': i + 1,
            'Title': title,
            'URL': product_url,
            'Price': price.text.strip() if price else 'N/A',
            'Rating': star_rating.text.strip()[2] if star_rating else 'N/A',
            'Reviews': ''.join(c for c in reviews.text.strip() if c.isdigit()) if reviews else 'N/A'
        }
        product_data_list.append(data)
    else:
        # This will run if the element is missing for a specific item (e.g., sponsored/ad item)
        print(f"❌ Skipping item (Likely an ad/filler).")

# --- CSV EXPORT ---
if product_data_list:
    # Use the keys from the first dictionary as the header row
    fieldnames = product_data_list[0].keys() 
    
    output_filename = 'amazon_phone_data.csv'
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader() # Writes the column headers
        writer.writerows(product_data_list) # Writes all the data rows
        
    print(f"\n🎉 Successfully saved {len(product_data_list)} products to {output_filename}")
else:
    print("\n⚠️ No product data was extracted to save.")