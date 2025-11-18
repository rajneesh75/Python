from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # make sure you have ChromeDriver
driver.get("https://quotes.toscrape.com/js/")

quotes = driver.find_elements(By.CLASS_NAME, "quote")

for q in quotes:
    print(q.find_element(By.CLASS_NAME, "text").text)

driver.quit()
