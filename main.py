from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from datetime import datetime, timedelta

driver = webdriver.Chrome()

print("Webpage is Loading...")
driver.get("https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&tracelog=newest")
time.sleep(1)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("Finished scrolling. Extracting data")

scraping_date = datetime.now().strftime("%d-%m-%Y")
rfq_items = driver.find_elements(By.CSS_SELECTOR, "div.brh-rfq-item")
data = []

for rfq in rfq_items:
    try:
        country_elem = rfq.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__country")
        try:
            country = country_elem.find_element(By.TAG_NAME, "img").get_attribute("alt").strip()
        except:
            country = country_elem.text.replace("Posted in:", "").strip()
    except:
        country = "N/A"

    try:
        buyer = rfq.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__other-info div.text").text.strip()
    except:
        buyer = "N/A"

    try:
        title = rfq.find_element(By.CSS_SELECTOR, "a.brh-rfq-item__subject-link").text.strip()
    except:
        title = "N/A"

    try:
        avatar_div = rfq.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__other-info div.avatar")
        img_elem = avatar_div.find_element(By.TAG_NAME, "img")
        img_src = img_elem.get_attribute("src")
        if img_src and img_src.startswith("//"):
            img_src = "https:" + img_src
    except:
        img_src = "N/A"

    try:
        qty_container = rfq.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__quantity")
        qty_number = qty_container.find_element(By.CSS_SELECTOR, "span.brh-rfq-item__quantity-num").text.strip()
        all_spans = qty_container.find_elements(By.TAG_NAME, "span")
        qty_unit = "N/A"
        for span in all_spans:
            if "Piece" in span.text or "Box" in span.text or "Pair" in span.text:
                qty_unit = span.text.strip()
                break
        quantity = f"{qty_number} {qty_unit}".strip()
    except:
        quantity = "N/A"

    try:
        quotes = rfq.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__quote-left span").text.strip()
    except:
        quotes = "N/A"

    try:
        inquiry_time = rfq.find_element(By.CSS_SELECTOR, "div.brh-rfq-item__publishtime").text.strip()
        inquiry_time = inquiry_time.replace("Date Posted:", "").strip()
    except:
        inquiry_time = "N/A"

    try:
        tags = rfq.find_elements(By.CSS_SELECTOR, "div.next-tag-body")
        tag_texts = [tag.text.lower() for tag in tags]
        email_confirmed = "Yes" if any("email confirmed" in tag for tag in tag_texts) else "No"
        experienced_buyer = "Yes" if any("experienced buyer" in tag for tag in tag_texts) else "No"
        complete_order = "Yes" if any("complete order via rfq" in tag for tag in tag_texts) else "No"
        typical_replies = "Yes" if any("typically replies" in tag for tag in tag_texts) else "No"
        interactive_user = "Yes" if any("interactive user" in tag for tag in tag_texts) else "No"
    except:
        email_confirmed = experienced_buyer = complete_order = typical_replies = interactive_user = "No"

    try:
        inquiry_url = rfq.find_element(By.CSS_SELECTOR, "a.brh-rfq-item__subject-link").get_attribute("href")
    except:
        inquiry_url = "N/A"

    try:
        if "p=ID" in inquiry_url:
            rfq_id = inquiry_url.split("p=ID")[-1].split("&")[0]
        else:
            rfq_id = "N/A"
    except:
        rfq_id = "N/A"
                

    try:
        if "day" in inquiry_time:
            days_ago = int(inquiry_time.split()[0])
            inquiry_date = (datetime.now() - timedelta(days=days_ago)).strftime("%d-%m-%Y")
        elif "hour" in inquiry_time.lower() or "minute" in inquiry_time.lower() or "just now" in inquiry_time.lower():
            inquiry_date = scraping_date
        else:
            inquiry_date = scraping_date
    except:
        inquiry_date = scraping_date

    data.append([
        rfq_id, title, buyer, img_src, inquiry_time, quotes, country,
        quantity, email_confirmed, experienced_buyer, complete_order,
        typical_replies, interactive_user, inquiry_url, inquiry_date, scraping_date
    ])

with open("alibaba_rfqs.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "RFQ ID", "Title", "Buyer Name", "Buyer Image", "Inquiry Time", "Quotes Left", "Country",
        "Quantity Required", "Email Confirmed", "Experienced Buyer", "Complete Order via RFQ",
        "Typical Replies", "Interactive User", "Inquiry URL", "Inquiry Date", "Scraping Date"
    ])
    writer.writerows(data)

driver.quit()
print("Data saved to alibaba_rfqs.csv")
