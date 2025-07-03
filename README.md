# Ekşi Sözlük Entry Scraper

This Python-based automation tool collects entries (posts) from the Turkish social media platform **Ekşi Sözlük** based on a keyword search and optional date range. The scraped data is saved into an Excel file and automatically merged with a master dataset.

## 📁 Project Structure

```
project-folder/
│
├── eksi_scraper.py           # Main script to search and extract entries
├── webdriver.py              # Manages Selenium WebDriver setup
├── excel_merger.py           # Merges new data into a main Excel file
├── date_formatter.py         # Standardizes date formats
└── README.md                 # Project documentation
```

---

## 🚀 Features

- Searches **Ekşi Sözlük** for a given keyword
- Supports **optional date filtering**
- Collects:
  - Entry content
  - Author name and profile
  - Post date and permalink
  - Topic title and ID
- Saves data to a structured Excel file
- Automatically merges into a central `standart.xlsx` file

---

## 🛠️ Dependencies

Install required Python libraries:

```bash
pip install selenium pandas openpyxl beautifulsoup4 requests
```

Also required:
- [Google Chrome](https://www.google.com/chrome/)
- Compatible version of [ChromeDriver](https://chromedriver.chromium.org/)

---

## ⚙️ Usage

### 1. Configure Driver Path

Update the following line in `eksi_scraper.py` to match your local `chromedriver.exe` path:

```python
driver_path = r"C:\Path\to\chromedriver.exe"
```

### 2. Run the Script

```bash
python eksi_scraper.py
```

You will be prompted to enter:
- A **keyword** to search (e.g., `deprem`, `ekonomi`)
- An optional **start and end date** in `YYYY-MM-DD` format (press Enter to skip)

### 3. Output

- An Excel file will be created in the format:
  ```
  keyword_entries.xlsx
  or
  keyword_2024-01-01_to_2024-01-31_entries.xlsx
  ```

- The result will be merged into `standart.xlsx` using `ExcelMerger`.

---

## 📌 Notes

- The scraper uses **Selenium** for dynamic topic link extraction and **BeautifulSoup** for fast entry parsing.
- Dates are normalized using `DateFormatter`.
- Duplicate entries are automatically avoided.
- Handles paginated topics and nested URLs efficiently.

---

## 📃 License

This project is for educational and personal research use only. Respect site terms and use responsibly.
