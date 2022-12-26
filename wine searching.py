#!/usr/bin/env python
# coding: utf-8

# In[173]:


import requests
import json
import ast
import urllib.parse
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
from itertools import groupby
from selenium.webdriver.common.keys import Keys
print('Finished importing packages.')
wine_list = ['Pomerol Wine', 'Cabernet Franc', 'Cabernet Sauvignon', 'Shiraz', 'Carmenere', 'Chateuaneuf du Pape', 'Cotes du Rhone',
            'Syrah', 'Merlot', 'Malbec']
short_wine_list = ['Pomerol Wine', 'Cabernet Franc', 'Cabernet Sauvignon']
def pd_max_options(rows, columns):
    pd.set_option('display.max_rows', rows)
    pd.set_option('display.max_columns', columns)
def df_where(df_name, column_name, value):
    return df_name.loc[df_name[column_name]==value]
    


# In[105]:


country_list = ['french']
id_list = []
name_list = []
wine_type_list = []
price_list = []
availability_list = []
for c in country_list:
    c_prop = c.title()
    print(f'Parsing {c_prop} wine.')
    num_list = []
    wine = wine.replace(' ', '-').lower()
    url = f'https://www.majestic.co.uk/{c}-wine?specs=75683&pagesize=32&orderby=111&pagenumber=1'
    s=Service('/Users/MatthewBeale/Desktop/chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    time.sleep(3)
    xpath_cookies = r'/html/body/div[4]/div[3]/div/div/div[2]/div/div/button'
    driver.find_element(By.XPATH, xpath_cookies).click()
    time.sleep(2)
    xpath_loc = r'/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span[1]'
    driver.find_element(By.XPATH, xpath_loc).click()
    xpath_postcode = r'/html/body/div[1]/div[3]/div/div[3]/div/div/div[2]/div[1]/input'
    time.sleep(2)
    postcode_entry = driver.find_element(By.XPATH, xpath_postcode)
    postcode_entry.click()
    postcode = 'N1 7HG'
    postcode_entry.send_keys(postcode)
    time.sleep(2)
    pc_confirm_xpath = r'/html/body/div[1]/div[3]/div/div[3]/div/div/div[2]/div[2]/button'
    driver.find_element(By.XPATH, pc_confirm_xpath).click()
    time.sleep(2)
    xpath_store = r'/html/body/div[1]/div[3]/div/div[3]/div/div/div[2]/div[4]/div[3]/div/a[1]/div'
    driver.find_element(By.XPATH, xpath_store).click()
    time.sleep(5)
    soup = bs(driver.page_source, 'html.parser')
    page_numbers = soup.find_all('li', class_ = lambda L: L and L.endswith('page'))
    if len(page_numbers) == 0:
        driver.get(url)
        #driver.find_element(By.XPATH, xpath_cookies).click()
        time.sleep(2)
        soup = bs(driver.page_source, 'html.parser')
        data = soup.find_all('a', class_ = 'product-name t-not-link')
        for item in data:
            #print('\n \n \n THE NEXT ONE \n \n \n')
            info = item.get('data-enhanced-productclick')
            info = info.strip()[15:]
            info = info.split(', "productUrl')[0]
            dic = ast.literal_eval(info)
            id_list.append(dic['id'])
            #print(dic['id'])
            name_list.append(dic['name'])
            wine_type_list.append(dic['brand'])
            price_list.append(dic['price'])
        data = soup.find_all('div', class_ = 'product-box-main')
        for item in data:
            if 'Not currently available at Majestic Islington.' in item.text:
                availability = 0
            else:
                availability = 1
            availability_list.append(availability)
    else:
        for item in page_numbers:
            try:
                num = int(item.text)
                num_list.append(num)
            except ValueError:
                continue
        print(num_list)
        max_num = max(num_list)
        final_num_list = list(range(1,max_num+1))
        print(final_num_list)
        for i in final_num_list:
            i = str(i)
            url = f'https://www.majestic.co.uk/{cunt}-wine?specs=75683&pagesize=32&orderby=111&pagenumber={i}'
            driver.get(url)
        #driver.find_element(By.XPATH, xpath_cookies).click()
            time.sleep(2)
            soup = bs(driver.page_source, 'html.parser')
            data = soup.find_all('a', class_ = 'product-name t-not-link')
            for item in data:
            #print('\n \n \n THE NEXT ONE \n \n \n')
                info = item.get('data-enhanced-productclick')
                info = info.strip()[15:]
                info = info.split(', "productUrl')[0]
                dic = ast.literal_eval(info)
                id_list.append(dic['id'])
                #print(dic['name'])
                name_list.append(dic['name'])
                wine_type_list.append(dic['brand'])
                price_list.append(dic['price'])
            data = soup.find_all('div', class_ = 'product-box-main')
            for item in data:
                if 'Not currently available at Majestic Islington.' in item.text:
                    availability = 0
                else:
                    availability = 1
                availability_list.append(availability)
    print(len(availability_list))
    print(len(id_list))
    driver.close()
df = pd.DataFrame({'id':id_list,
                  'name':name_list,
                  'type':wine_type_list,
                  'price':price_list,
                  'availability': availability_list})
df = df.drop_duplicates()

    
    
    
    


# In[189]:


pd_max_options(500,500)
df = df_where(df, 'availability', 1)
df
viv_rat_list = []
num_ratings_list = []
viv_price_list = []
rate_list = df['name'].to_list()
rate_url = 'https://www.vivino.com/GB/en/'
for wine in rate_list:
    s=Service('/Users/MatthewBeale/Desktop/chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get(rate_url)
    xpath_cookies = r'/html/body/div[2]/div[7]/div/button/span'
    time.sleep(2)
    driver.find_element(By.XPATH, xpath_cookies).click()
    time.sleep(2)
    xpath_search = r'/html/body/div[2]/div[1]/div/nav/div[1]/div/div/div/form/input'
    search = driver.find_element(By.XPATH, xpath_search)
    search.click()
    time.sleep(1)
    search.send_keys(wine)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    soup = bs(driver.page_source, 'html.parser')
    try:
        data = soup.find('div', class_ = "text-inline-block light average__number")
        rating = data.text.strip()
        viv_rat_list.append(rating)
    except AttributeError:
        viv_rat_list.append(None)
    try:
        data = soup.find('p', class_ = "text-micro")
        num_ratings = data.text.strip().split(' ')[0]
        num_ratings_list.append(num_ratings)
    except AttributeError:
        num_ratings_list.append(None)
    try:
        data = soup.find('span', class_ = 'wine-price-value')
        price = data.text.strip()
        if price == '-':
            viv_price_list.append(None)
        else:
            viv_price_list.append(price)
    except AttributeError:
        viv_price_list.append(None)
    driver.close()
#print(viv_rat_list)
print(len(viv_rat_list))
#print(num_ratings_list)
print(len(num_ratings_list))
#print(viv_price_list)
print(len(viv_price_list))
rate_df = pd.DataFrame({'name':rate_list,
                       'viv_rating':viv_rat_list,
                       'num_viv_ratigns':num_ratings_list,
                       'viv_price':viv_price_list})


# In[192]:


fin_df = df.merge(rate_df, how='inner', on='name')
fin_df


# In[193]:


fin_df.to_csv('/Users/matthewbeale/Documents/Python/Wine/french_wine.csv', index=False, encoding = 'utf-8-sig')


# In[ ]:




