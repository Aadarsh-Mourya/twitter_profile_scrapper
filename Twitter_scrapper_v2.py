import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse

# Function to initialize the Selenium WebDriver with options
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    service = Service(executable_path=r"chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to validate Twitter profile URL
def validate_twitter_url(url):
    valid_domains = [
            'twitter.com',
            'www.twitter.com',
            'x.com',
            'www.x.com'
        ]
    try:
        parsed = urlparse(url)
        if not parsed.netloc in valid_domains:
            return False
        
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) == 0 or not path_parts[0]:
            return False
            
        return True
    except:
        return False

# Function to scrape a single Twitter profile URL
def scrape_twitter_profile(driver, url):
    if not validate_twitter_url(url):
        return {
            "Profile URL": url,
            "Status": "Invalid URL",
            "Username": "",
            "Display Name": "",
            "Bio": "",
            "Following Count": "",
            "Followers Count": "",
            "Location": "",
            "Website": ""
        }
    
    data = {
        "Profile URL": url,
        "Status": "Success",
        "Username": "",
        "Display Name": "",
        "Bio": "",
        "Following Count": "",
        "Followers Count": "",
        "Location": "",
        "Website": ""
    }
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10) # wait for 10 seconds for elements to load
        
        # extract username
        try:
            username_elem = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="UserName"]')
            ))
            username_text = username_elem.text
            if "@" in username_text:
                data["Username"] = username_text.split("@")[-1].strip()
            else:
                data["Username"] = username_text.strip()
        except TimeoutException:
            data["Username"] = "not found"
        
        # Extract Display Name
        try:
            name_elem = username_elem.find_element(By.TAG_NAME, 'span')
            data["Display Name"] = name_elem.text.strip() if name_elem else "not found"
        except Exception:
            data["Display Name"] = "Element not found"
        
        # Extract Bio
        try:
            bio_elem = driver.find_element(By.CSS_SELECTOR, '[data-testid="UserDescription"]')
            data["Bio"] = bio_elem.text.strip() if bio_elem else "not found"
        except NoSuchElementException:
            data["Bio"] = "Element not found"
        
        # Extract Following Count
        try:
            following_elem = driver.find_element(By.XPATH, '//a[contains(@href, "/following")]/span[1]//span')
            data["Following Count"] = following_elem.text.strip() if following_elem else "not found"
        except NoSuchElementException:
            data["Following Count"] = "Element not found"
        
        # Extract Followers Count
        try:
            followers_elem = driver.find_element(By.XPATH, '//a[contains(@href, "/verified_followers")]/span[1]//span')
            data["Followers Count"] = followers_elem.text.strip() if followers_elem else "not found"
        except NoSuchElementException:
            data["Followers Count"] = "Element not found"
        
        # Extract Location
        try:
            location_elem = driver.find_element(By.XPATH, '//span[contains(@data-testid,"UserLocation")]//span')
            data["Location"] = location_elem.text.strip() if location_elem else "not found"

        except NoSuchElementException:
            data["Location"] = "Element not found"
        
        # Extract Website
        try:
            website_elem = driver.find_element(By.XPATH, '//a[contains(@href, "http") and not(contains(@href, "twitter.com")) and not(contains(@href, "x.com"))]')
            data["Website"] = website_elem.get_attribute("href").strip() if website_elem else "not found"
        except NoSuchElementException:
            data["Website"] = "not found"
            
    except TimeoutException:
        data["Status"] = "Timeout Error"
    except Exception as e:
        data["Status"] = f"Error: {str(e)}"
    
    return data

# Streamlit UI code
def main():
    st.title("Twitter Profile Scraper")
    st.write("Upload a CSV file containing a column of Twitter profile URLs.")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df_input = pd.read_csv(uploaded_file)

            if 'Profile URL' not in df_input.columns:
                st.error("CSV file must have a column named 'Profile URL'.")
                return
            st.write("Input URLs:")
            st.dataframe(df_input, use_container_width=True) # Display the input DataFrame
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            return
        
        if st.button("Scrape Profiles"):
            driver = init_driver() # Initialize Selenium driver
            scraped_data = []
            valid_urls = []
            invalid_urls = []
            
            # Validate URLs and separate valid and invalid ones
            for idx, row in df_input.iterrows():
                url = row['Profile URL']
                if validate_twitter_url(url.lstrip('@')):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
            
            # Display invalid URLs
            if invalid_urls:
                st.warning(f"Found {len(invalid_urls)} invalid URLs. They will be skipped.")
                st.write("Invalid URLs:", invalid_urls)
            
            total = len(valid_urls)
            progress_text = "Scraping in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)
            
            # Scrape each valid URL
            for idx, url in enumerate(valid_urls):
                st.write(f"Scraping {url}...")
                profile_data = scrape_twitter_profile(driver, url)
                scraped_data.append(profile_data)
                my_bar.progress((idx + 1) / total)
            
            driver.quit() # Close the browser window

            # Create a DataFrame from the scraped data
            df_output = pd.DataFrame(scraped_data)
            output_csv = "scraped_twitter_profiles.csv"
            df_output.to_csv(output_csv, index=False)
            
            st.success("Scraping completed!")
            st.write("Scraped Data:")
            st.dataframe(df_output, use_container_width=True)
            st.download_button(
                label="Download CSV",
                data=df_output.to_csv(index=False).encode('utf-8'),
                file_name=output_csv,
                mime='text/csv'
            )

if __name__ == '__main__':
    main()