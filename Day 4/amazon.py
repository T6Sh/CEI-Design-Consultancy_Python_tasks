import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha

api_key = 'YOUR_2CAPTCHA_API_KEY'

def solve_captcha(driver):
    solver = TwoCaptcha(api_key)
    try:
        result = solver.solve_captcha(driver.current_url)
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{result}'")
        driver.execute_script("document.getElementById('g-recaptcha').dispatchEvent(new Event('change'))")
    except Exception as e:
        print(f"Error solving CAPTCHA: {e}")

def dismiss_popups(driver):
    try:
        dismiss_buttons = driver.find_elements(By.CSS_SELECTOR, "button.close, button.dismiss, .popup-close, .a-popover-close")
        for button in dismiss_buttons:
            button.click()
        time.sleep(1)
    except Exception as e:
        print(f"No pop-up found or error occurred: {e}")

def scrape_amazon_category(category_name, num_products=100):
    base_url = "https://www.amazon.in/s"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(base_url)

    try:
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_bar.send_keys(category_name)
        search_bar.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error finding search bar: {e}")
        driver.quit()
        return []

    time.sleep(2)

    product_links = []
    page_number = 1

    while len(product_links) < num_products:
        dismiss_popups(driver)

        if driver.find_elements(By.CSS_SELECTOR, ".captcha-container"):
            solve_captcha(driver)
        
        products = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")
        for product in products:
            try:
                name_element = product.find_element(By.CSS_SELECTOR, "h2 a span")
                link_element = product.find_element(By.CSS_SELECTOR, "h2 a")
                product_name = name_element.text
                product_link = link_element.get_attribute('href')
                
                if '/dp/' in product_link and product_link not in [link[1] for link in product_links]:
                    product_links.append((product_name, product_link))
                    if len(product_links) >= num_products:
                        break
            except Exception as e:
                continue

        if len(product_links) >= num_products:
            break

        page_number += 1
        next_page_url = f"{base_url}?k={category_name.replace(' ', '+')}&page={page_number}"
        driver.get(next_page_url)
        time.sleep(5)
    
    driver.quit()
    return product_links[:num_products]

def scrape_multiple_categories(categories, num_products_per_category=100):
    all_product_links = []
    serial_no = 1

    for category in categories:
        print(f"Scraping category: {category}")
        product_links = scrape_amazon_category(category, num_products=num_products_per_category)
        for product_name, product_link in product_links:
            main_name, *specs = product_name.split(",", 1)
            specification = specs[0] if specs else ""
            all_product_links.append([serial_no, category, main_name, specification, product_link])
            serial_no += 1
        print(f"Found {len(product_links)} products for category: {category}")
    
    return all_product_links

def save_to_csv_via_dataframe(all_product_links, filename="products.csv"):
    df = pd.DataFrame(all_product_links, columns=["Serial No", "Category", "Name", "Specification", "Link"])
    print(df)  # Print the DataFrame
    df.to_csv(filename, index=False, encoding='utf-8')  # Convert DataFrame to CSV
    print(f"\nCSV file '{filename}' created successfully with {len(df)} products.")

categories = ['Handbags', 'Bath & Skin Care', 'Ayurveda', 'Routers', 'Home Health Tests', 'Outdoor Adventure Gear', 'Bike Accessories', 'Vitamins']
all_links = scrape_multiple_categories(categories)

save_to_csv_via_dataframe(all_links)
