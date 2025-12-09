from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Setup the Driver (Using WebDriver Manager)
# This finds and sets up the correct driver for your Chrome version
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 2. Define the URL (Use a specific product URL for initial testing)
URL = 'https://www.amazon.in/Samsung-Awesome-Storage-Nightography-Corning/dp/B0CWPDH74H/ref=sr_1_3?crid=1EHWVAQAUL4UB&dib=eyJ2IjoiMSJ9.9g6QgUDkU4-WXHXxTLL_EPK4dQrvJ8T4P8LanwxvaTOwKawSLHFdaUr7rHc0stPgM69-iN3jokO3djJbdOgDs4fqfHkym_4jIuF-KR5cq7K16yFNjyflyzvLzrwX7E1ulSQgsZZnmMrE79Chcn2ffgyiAfhKSQcJrW4b7OUNk9DUajC7kUCPF5Uvw7nEKhmGhNGkELKeS9i_vKC2mRrynripjiSJXnUMqTBR7TSuIg8.y0opgeEda6ThfAXb6LmIDCSLi4gdiMn3kD-8JuhvlQE&dib_tag=se&keywords=phones&qid=1765202276&sprefix=phone%2Caps%2C215&sr=8-3&th=1' # Replace with a test URL

# 3. Open the browser and navigate
driver.get(URL)

# --- CRUCIAL STEP: WAIT FOR DYNAMIC CONTENT ---
# We wait up to 10 seconds for a specific element (like the main price) 
# to appear before proceeding. Replace 'your-price-element-id' with a real selector.
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'priceblock_ourprice')) # Example ID, may not be current
    )
except Exception:
    print("Timed out waiting for content to load.")
    # You might need to adjust the wait time or the element selector

# 4. Capture the fully rendered HTML
html_content = driver.page_source

# 5. Close the browser
driver.quit()

# 6. Parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
print(soup.prettify())  # Optional: Print the prettified HTML for inspection
# 7. Extract the desired data
# (This step depends entirely on the specific Amazon page's HTML structure)
# Example: Find a main title
product_title = soup.find('span', {'id': 'productTitle'})

if product_title:
    print("Product Title:", product_title.text.strip())
else:
    print("Could not find product title. Check your selector.")