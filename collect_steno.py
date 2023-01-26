#%%

import re

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

STENO_PAGE = 'https://www.senat.ro/stenogramecalendar.aspx?Plen=1'

# %%
options = Options()
# %%

# %%
# Init driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(1)

# %%
def access_steno_page():
    """ """
    try:
        driver.get(STENO_PAGE)
    except:
        print('Couldn\'t access page.')
# %%

def provide_year(year: int):
    """ Given a specific year, modify the input field such that the page displayed is appropriate """
    date_input_xpath = '//*[@id="ctl00_B_Center_StenogrameCalendar_txtAn"]'

    try:
        date_input_element = driver.find_element(By.XPATH, date_input_xpath)
    except: 
        print('Couldn\'t find input element.')

    date_input_element = driver.find_element(By.XPATH, date_input_xpath)
    date_input_element.clear()
    date_input_element.send_keys(year)
    date_input_element.send_keys(Keys.RETURN)

def extract_page_source():

    soup = BeautifulSoup(driver.page_source, features='html.parser')

    return soup


def get_date_steno_url_pairs(soup):
    """ Given a bs4 soup return the steno urls and the corresponding dates """
    calendar_table = soup.find_all('table', attrs = {'style':"margin-left:auto; margin-right:auto;"})[0]
    calendar_date_a_tags = calendar_table.find_all('a')


    collector_dict = {}

    for idx, tag in enumerate(calendar_date_a_tags):
        
        day = re.findall('\d+', tag.text)[0]
        steno_type = tag.text.split(day)[1].strip()
        if not steno_type:
            steno_type = 'normal' 
        
        
        month = tag.parent.parent.parent.find_all('tbody')[0].text.strip()

        href = tag['href']
        collector_dict[idx] = dict(day = day, month = month, type = steno_type, href = href)

    return collector_dict



if __name__=="__main__":
    pass

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
