from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import requests
from date_formatter import DateFormatter
from excel_merger import ExcelMerger
from webdriver import WebDriverManager


def get_search_url(keyword, start_date=None, end_date=None):
    keyword_formatted = '+'.join(keyword.split())
    base_url = f"https://eksisozluk.com/basliklar/ara?SearchForm.Keywords={keyword_formatted}&SearchForm.SortOrder=Date"
    if start_date and end_date:
        base_url += f"&SearchForm.When.From={start_date}&SearchForm.When.To={end_date}"
    return base_url


def get_eksi_links(search_url, driver, wait):
    driver.get(search_url)
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='topic-list']")))

    links = []
    try:
        while True:
            elements = driver.find_elements(By.XPATH, "//ul[@class='topic-list']/li/a")
            for element in elements:
                link = element.get_attribute('href')
                if link:
                    links.append(link)
            try:
                more_button = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".full-index-continue-link-container a")))
                driver.execute_script("arguments[0].click();", more_button)
                continue
            except:
                get_next_buttons = driver.find_elements(By.CSS_SELECTOR, ".pager .next")
                if get_next_buttons:
                    driver.execute_script("arguments[0].click();", get_next_buttons[-1])
                else:
                    break
            wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='topic-list']/li/a")))
    except:
        driver.close()
    return links


def scrape_entries(url, formatter):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    social_media_ids = []
    title_ids = []
    entries = []
    entry_dates = []
    entry_authors = []
    entry_links = []
    entry_ids = []
    titles = []
    user_links = []

    page_number = 1
    while True:
        page_url = f"{url}&p={page_number}" if '?' in url else f"{url}?p={page_number}"
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        entry_elements = soup.find_all('div', class_='content')
        if not entry_elements:
            break

        for entry in entry_elements:
            social_media_ids.append("8")
            entries.append(entry.text.strip())

            entry_date = entry.parent.find('a', class_='entry-date permalink').text
            entry_dates.append(formatter.format_eksi(entry_date))

            entry_author = entry.parent.find('a', class_='entry-author').text
            entry_authors.append(entry_author)

            entry_link = 'https://eksisozluk.com' + entry.parent.find('a', class_='entry-date permalink')['href']
            entry_links.append(entry_link)

            entry_id = entry.parent.find('a', class_='entry-date permalink')['href'].split('/')[-1]
            entry_ids.append(entry_id)

            title = soup.find('h1', id='title').text.strip()
            titles.append(title)

            title_id = url.split('--')[-1].split('?')[0]
            title_ids.append(title_id)

            user_link = 'https://eksisozluk.com' + entry.parent.find('a', class_='entry-author')['href']
            user_links.append(user_link)

        page_number += 1

    return social_media_ids, title_ids, entries, entry_dates, entry_authors, entry_links, entry_ids, titles, user_links


def save_to_excel(data, title, start_date=None, end_date=None):
    if start_date and end_date:
        date_range = f"{start_date}_to_{end_date}"
        excel_filename = f"{title}_{date_range}_entries.xlsx"
    else:
        excel_filename = f"{title}_entries.xlsx"

    df = pd.DataFrame(data, columns=[
        'SocialMediaId', 'PostId', 'Text', 'PostDate', 'Name', 'TextUrl', 'CommentId', 'Title', 'ProfileUrl'
    ])
    df.to_excel(excel_filename, index=False)
    print(f"Entries successfully saved to {excel_filename}")
    return excel_filename


def main():
    keyword = input("Enter a keyword to search on Ekşi Sözlük: ")
    start_date = input("Enter the start date (YYYY-MM-DD) or press Enter to ignore: ")
    end_date = input("Enter the end date (YYYY-MM-DD) or press Enter to ignore: ")

    driver_path = r"C:\Users\soytu\OneDrive\Masaüstü\program\chromedriver.exe"

    web_driver_manager = WebDriverManager(driver_path=driver_path)
    driver, wait = web_driver_manager.initialize_driver()

    search_url = get_search_url(keyword, start_date, end_date)
    entry_links = get_eksi_links(search_url, driver, wait)

    all_data = []
    formatter = DateFormatter()
    merger = ExcelMerger("standart.xlsx")
    title = keyword.replace(" ", "_")

    for url in entry_links:
        scraped = scrape_entries(url, formatter)
        if not scraped[0]:
            continue
        social_media_ids, title_ids, entries, entry_dates, entry_authors, entry_links, entry_ids, titles, user_links = scraped
        for idx in range(len(title_ids)):
            row = {
                'SocialMediaId': social_media_ids[idx],
                'PostId': title_ids[idx],
                'Text': entries[idx],
                'PostDate': entry_dates[idx],
                'Name': entry_authors[idx],
                'TextUrl': entry_links[idx],
                'CommentId': entry_ids[idx],
                'Title': titles[idx],
                'ProfileUrl': user_links[idx]
            }
            all_data.append(row)

    if all_data:
        excel_filename = save_to_excel(all_data, title, start_date, end_date)
        merger.merge(excel_filename)
        merger.save("standart.xlsx")
    else:
        print("No entries found.")

if __name__ == "__main__":
    main()
