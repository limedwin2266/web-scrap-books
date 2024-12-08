import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import mysql.connector
import pandas as pd
#---------------------------- CONSTANTS ------------------------------- #
BOOK_URL = "https://www.mysiswaplace.my/mysiswa#?lang=MS"
FORM_LINK= "https://forms.gle/ePzV3psdGR2sqwQw8"

#---------------------------- SELENIUM ------------------------------- #
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(BOOK_URL)
driver.maximize_window()

book_search = driver.find_element(By.ID, value="glo_sch")
book_search.send_keys("[大众书局]")
search_btn = driver.find_element(By.ID, value="btn-sch")
search_btn.click()

# Wait for the search results to load
time.sleep(5)


while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        # Wait for the button to be present
        load_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "loadMore"))
        )
        load_btn.click()  # Click the button
        time.sleep(5)  # Allow time for content to load
    except TimeoutException:
        # Break the loop if the button is not found
        print("No 'Load More' button found. Exiting loop.")
        break
#Get the page source
page_source=driver.page_source

# ---------------------------- BEAUTIFULSOUP ------------------------------- #
soup = BeautifulSoup(page_source,"html.parser")
all_book = soup.find_all('div', class_='book_title')
all_price = soup.find_all('span', class_="one-unit-price")
book_lst=[book.text.strip() for book in all_book]
price_lst = [price.text.strip() for price in all_price]

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="edwinlim0926",
    database="popular_db",
    charset='utf8mb4'
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE books(
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(1000) CHARACTER SET utf8mb4,
    price VARCHAR(100)
)
''')

for data in range(len(book_lst)):

    title = book_lst[data]
    price = price_lst[data]
    title = title.encode('utf-8').decode('utf-8')

    cursor.execute(f'''
    INSERT INTO books (title, price)
    VALUES (%s, %s);
    ''', (title, price))

conn.commit()
conn.close()
# ========================== Connect to SQL Server =================================
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="edwinlim0926",
    database="popular_db",
    charset='utf8mb4'
)
cursor = conn.cursor()
cursor.execute("SELECT title, price FROM books")
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=["Book Title", "Price"])
df.to_csv('books_utf8sig.csv', index=False, encoding='utf-8-sig')

print("Data has been inserted into the MySQL database.")

conn.close()