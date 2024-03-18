import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import re 
import time




def remove_extra_whitespace(text):
    return re.sub(r'\s+', ' ', text)


def Send_Request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestsWarning as e:
        print(e)


def Scraping(text):
    soup = BeautifulSoup(text, "html.parser")

    inner_divs = soup.find_all('div', class_ = 'right_radius_change')
    for info in inner_divs:
        job_name = remove_extra_whitespace(info.find('p', class_ = "font_bold").text.strip())
        company = remove_extra_whitespace(info.find('p', class_ = "job_list_company_title").text.strip())
        deadline = remove_extra_whitespace(info.find('div', class_ = 'badge_deadline_block').text.strip())
        location = remove_extra_whitespace(info.find('p', class_ = "job_location").text.strip())
        DataFrame.loc[len(DataFrame.index)] = [job_name, company, deadline, location]


def Scrap_Whole_Pages():
    driver = webdriver.Chrome()
    driver.get(url)

    Job = driver.find_element(By.ID, 'w1').find_element(By.CLASS_NAME, "hs_nav_link")
    Job.click()

    Scraping(driver.page_source)



    next = driver.find_element(By.CLASS_NAME, 'pagination').find_element(By.CLASS_NAME, 'next')
    while True:
        Scraping(driver.page_source)
        if 'disabled' in next.get_attribute('class'):
            break
        print(next.is_enabled())
        next.click()
        time.sleep(1)
        
        
        next = driver.find_element(By.CLASS_NAME, 'pagination').find_element(By.CLASS_NAME, 'next')
    driver.quit()
    return
    
    
if __name__  == "__main__":
    url = "https://staff.am/en"
    DataFrame = pd.DataFrame(columns = ["Job_Name", "Company", "Deadline", "Location"])
    Scrap_Whole_Pages()
    DataFrame.to_csv("Job_am_data", index=False)
    print(DataFrame)