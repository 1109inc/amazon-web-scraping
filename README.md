# 📱 Amazon Search Results Scraper

This is a small, proof-of-concept project designed to demonstrate robust web scraping techniques on dynamic, anti-bot protected websites, specifically Amazon search results.

The script automates the process of loading a search results page, extracting structured data, and handling common structural inconsistencies found in product listings.

---

## ⚙️ Technologies Used

| Tool              | Purpose                                                                                                                                 |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **Python**        | Primary development language.                                                                                                           |
| **Selenium**      | Used to launch a Chrome browser, handle dynamic content loading (JavaScript), and bypass basic anti-bot defenses (user-agent spoofing). |
| **BeautifulSoup** | Used for efficient parsing of the captured HTML source code, allowing for targeted data extraction using CSS class selectors.           |
| **CSV**           | Used to save the final structured data to a universal file format.                                                                      |

---

## 🚀 Data Extracted (Example Fields)

The scraper successfully extracts key details for the majority of products (organic listings and many ads) found on the search results page:

- **Title**
- **Product URL**
- **Price**
- **Rating**
- **Review Count**

---

## ▶️ Demo Video

As the HTML structure of the target website is subject to frequent change, this video confirms the successful execution of the scraper and the generation of structured data as of the recording date:

[Watch the Scraper in Action](https://youtu.be/5VkigwZWokY)

---

## Note - main.py is sample for testing on a single product instead of list, go through it before running list_scrape

## 🏃 How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/1109inc/amazon-web-scraping
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the script:**
    ```bash
    python list_scrape.py
    ```
