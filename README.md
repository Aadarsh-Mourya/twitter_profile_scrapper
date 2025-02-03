# Twitter Profile Scraper

This project is a Python-based Twitter profile scraper that leverages Selenium for web automation and Streamlit for creating a simple user interface. The script reads a CSV file containing Twitter profile URLs, scrapes profile information (such as username, display name, bio, following/followers counts, location, and website), and outputs the data as a downloadable CSV file.

## Features

- **Automated Scraping:** Uses Selenium to navigate Twitter profiles and extract relevant data.
- **URL Validation:** Ensures only valid Twitter or X (formerly Twitter) URLs are processed.
- **Streamlit UI:** Provides a clean web interface for file uploads, progress tracking, and viewing/downloading results.
- **Error Handling:** Gracefully handles missing elements and timeouts during scraping.

## Prerequisites

- **Python 3.7+**: Make sure Python is installed.
- **Chrome WebDriver:** Download the appropriate version of [ChromeDriver](https://chromedriver.chromium.org/downloads) for your Chrome browser and ensure it is in your system's PATH or update the `executable_path` in the code accordingly.
- **Internet Connection:** Required for accessing Twitter profiles.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/twitter-profile-scraper.git
   cd twitter-profile-scraper


2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare your CSV file:**

   Ensure your CSV file contains a column named `Profile URL` with the Twitter profile URLs you want to scrape.

2. **Run the Streamlit app:**

   ```bash
   streamlit run your_script.py
   ```

   Replace `your_script.py` with the name of your Python file containing the code.

3. **Interact with the UI:**

   - Upload your CSV file using the provided file uploader.
   - Click the "Scrape Profiles" button to start the scraping process.
   - View the results directly in the web interface and download the CSV file containing the scraped data.

## Code Structure

- **init_driver():** Initializes a headless Chrome WebDriver.
- **validate_twitter_url(url):** Validates that the URL is from Twitter or X and contains a valid profile path.
- **scrape_twitter_profile(driver, url):** Scrapes the Twitter profile page and extracts required information.
- **main():** Implements the Streamlit UI for file upload, progress tracking, and output display.

## License

This project is licensed under the MIT License. See the [LICENSE] file for details.
