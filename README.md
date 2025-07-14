# Alibaba RFQ Scraper 🇦🇪

This is a Python web scraper using Selenium to extract real-time RFQ (Request for Quotation) data from Alibaba's sourcing portal. It targets RFQs posted from the United Arab Emirates and exports the data into a structured CSV file.

## 🔍 Features

- Scrolls and loads all RFQs on the page automatically
- Extracts key fields such as:
  - RFQ ID
  - Title
  - Buyer Name
  - Buyer Image
  - Inquiry Time & Date
  - Quantity Required
  - Country
  - Email Verified, Buyer Experience, Tags
  - Inquiry URL
  - Inquiry Date
  - Scraping Date

- Outputs data into `alibaba_rfqs.csv`

## 📦 Requirements

- Python 3.7+
- Google Chrome browser
- ChromeDriver

Install dependencies:
```bash
pip install selenium
```

🚀 Usage
```bash
python alibaba_scraper.py
```

📝 Output
The resulting alibaba_rfqs.csv file contains the following columns:

  - RFQ ID
  - Title
  - Buyer Name
  - Buyer Image
  - Inquiry Time & Date
  - Quantity Required
  - Country
  - Email Verified, Buyer Experience, Tags
  - Inquiry URL
  - Inquiry Date
  - Scraping Date


