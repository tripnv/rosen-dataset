#%%
import os
import re
import json
import requests
from time import sleep
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import argparse
#%%
BASE_URL = 'https://senat.ro/'
STENO_PAGE = 'https://www.senat.ro/stenogramecalendar.aspx?Plen=1'
STENO_LOGS_PATH = 'steno_logs/'
STENO_DIR = 'steno_pdfs/'

# %%
def access_steno_page(driver):
    """ """
    try:
        driver.get(STENO_PAGE)
    except:
        print('Couldn\'t access page.')
# %%

def decrease_year(driver):
    """ Decrease the year, by clicking the button """
    decrease_button_xpath = '//*[@id="ctl00_B_Center_StenogrameCalendar_txtAn_bDown"]'
    
    try:
        decrease_button_element = driver.find_element(By.XPATH, decrease_button_xpath)
    except: 
        print('Couldn\'t find button element.')

   
    decrease_button_element.click()
    sleep(1)


def extract_page_source(driver):

    soup = BeautifulSoup(driver.page_source, features='html.parser')

    return soup


def get_date_steno_url_pairs(soup, year):
    """ Given a bs4 soup return the steno urls and the corresponding dates """
    calendar_table = soup.find_all('table', attrs = {'style':"margin-left:auto; margin-right:auto;"})[0]
    calendar_date_a_tags = calendar_table.find_all('a')


    collector_dict = {}

    for idx, tag in enumerate(calendar_date_a_tags):
        
        day = re.findall('\d+', tag.text)[0]
        
        steno_type = tag.text.split(day)[1].strip()
        if int(day) < 10:
            day = '0' + str(day)

        if not steno_type:
            steno_type = 'normal' 
        
        
        month = tag.parent.parent.parent.find_all('tbody')[0].text.strip()

        href = BASE_URL + tag['href']
        collector_dict[idx] = dict(
            day = day, 
            month = month,
            full_date = f"{str(day)}_{month}_{year}",
            type = steno_type, 
            href = href)

    return collector_dict

def save_steno_dict(steno_dict, year):
    
    with open(f'{STENO_LOGS_PATH}log_{year}', 'w') as f:
        json.dump(steno_dict, f, indent = 4)

#%%

if __name__=="__main__":

    # parser = argparse.ArgumentParser()    
    # parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
    # args = parser.parse_args()

    # years_str = args.list
    # years_int = [int(year) for year in years_str]


    options = Options()
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(5)
    access_steno_page(driver = driver)

    for idx in range(3):
        year = 2023 - (idx + 1)

        decrease_year(driver)

        soup_1 = extract_page_source(driver)
        year_steno_dict = get_date_steno_url_pairs(soup_1, year=year)
        save_steno_dict(year_steno_dict, year)


        downloaded_stenos = 0
        full_folder_path = f"{STENO_DIR}/{year}"
        os.makedirs(full_folder_path)
        
        for idx, (steno_idx, steno_log) in tqdm(enumerate(year_steno_dict.items())):
            url = steno_log['href']
            
            

            fname = f"{full_folder_path}/steno_{idx}_{steno_log['full_date']}.pdf"

            try:
                response = requests.get(url)
            
                with open(fname, 'wb') as f:
                    f.write(response.content)
                downloaded_stenos += 1
                sleep(2)

            except:
                pass
        print(f"Downloaded {downloaded_stenos} stenograms out of {len(year_steno_dict)} for year {year}.")











# access_steno_page(driver = driver)
# #%%
# for year in years_int:
#     print(year)
#     driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)

#     driver.implicitly_wait(5)
#     access_steno_page(driver = driver)
#     sleep(5)
#     provide_year(driver=driver, year = year)

#     soup_1 = extract_page_source(driver)
#     year_steno_dict = get_date_steno_url_pairs(soup_1, year=year)
#     save_steno_dict(year_steno_dict, year)

#         # downloaded_stenos = 0
#         # full_folder_path = f"{STENO_DIR}/{year}"
#         # os.makedirs(full_folder_path)
#         # sleep(5)
#         # for idx, (steno_idx, steno_log) in tqdm(enumerate(year_steno_dict.items())):
#         #     url = steno_log['href']
            
            

#         #     fname = f"{full_folder_path}/steno_{idx}_{steno_log['full_date']}.pdf"

#         #     try:
#         #         response = requests.get(url)
            
#         #         with open(fname, 'wb') as f:
#         #             f.write(response.content)
#         #         downloaded_stenos += 1
#         #         sleep(2)

#         #     except:
#         #         pass
#         # print(f"Downloaded {downloaded_stenos} stenograms out of {len(year_steno_dict)} for year {year}.")



# calendar_xpath = '//*[@id="ctl00_B_Center_StenogrameCalendar_panou"]/table/tbody/tr[2]/td/div/table'
# # # %%
# # try: 
# #     calendar_element = driver.find_element(By.XPATH, calendar_xpath)
# # except:
# #     print('Couldn\'t find calendar.')
# # %%


# get_date_steno_url_pairs(soup)


# # %%
# x = calendar_element.get_attribute('href')
# # %%
# calendar_href_elements = calendar_element.find_elements(By.XPATH, ".//a[@href]")
# calendar_href_parents =  calendar_element.find_elements(By.XPATH, ".//a[@href]/../../..")
# # %%

# calendar_href_parents
# # %%
# [p.text for p in calendar_href_parents]
# # %%
# len(calendar_href_parents)
# # %%
# calendar_href_elements[0].

# # %%
# driver.page_source
# # %%
# # %%
# soup = BeautifulSoup(driver.page_source, features='html.parser')
# # %%

# for idx, table in enumerate(soup.find_all('table', attrs = {'style':"margin-left:auto; margin-right:auto;"})):
#     print(table.text)
# # %%
# calendar_table = soup.find_all('table', attrs = {'style':"margin-left:auto; margin-right:auto;"})[0]
# # %%
# calendar_date_a_tags = calendar_table.find_all('a')
# # %%
# [cdat['href'] for cdat in calendar_date_a_tags]
# # %%
# sample_tag = calendar_date_a_tags[0]
# # %%

# steno_month = sample_tag.parent.parent.parent.find_all('tbody')[0].text.strip()
# # %%
# sample_tag.text
# # %%

# %%
