from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
import warnings
from pymongo import MongoClient
import requests
import re
import json

warnings.simplefilter('ignore')

cu_path = os.getcwd()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}

client = MongoClient('localhost', 27017)

def q2():
  print(cu_path + "/chromedriver")
  driver = webdriver.Chrome(executable_path= cu_path + "/chromedriver")
  driver.implicitly_wait(10)
  driver.set_script_timeout(120)
  driver.set_page_load_timeout(10)
  driver.get("https://opensea.io/collection/boredapeyachtclub?search[sortAscending]=false&search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold")
  data = driver.find_element(By.CLASS_NAME, "sc-f83e23d1-0.ghvfYp")
  all_links = data.find_elements(By.CLASS_NAME, "sc-29427738-0.sc-e7851b23-1.dVNeWL.hfa-DJE.Asset--loaded")
  print(len(all_links))
  links_eights = all_links[:8]
  link_list = []
  for i in links_eights:
    link = i.find_element(By.CLASS_NAME ,"sc-1f719d57-0.fKAlPV.Asset--anchor").get_attribute('href')
    link_list.append(link)
  for num , each_link in enumerate(link_list):
    num = num + 1
    time.sleep(3)
    driver.get(each_link)
    with open(f"bayc_{num}.htm", "w", encoding = 'utf-8') as file:
      file.write(driver.page_source)
  driver.quit()


def q3():
  mydatabase = client['bayc']
  mycollection = mydatabase['bayc']
  mycollection.drop()
  for i in range(1,9):
    file_name = f"bayc_{i}.htm"
    with open(file_name , "r" , encoding = 'utf-8') as f:
      contents = f.read()
      soup = BeautifulSoup(contents, 'lxml')
      title_name = soup.select("h1.sc-29427738-0.hKCSVX.item--title")[0].text
      # attributes = soup.select("div.sc-29427738-0.hKCSVX.item--title > div.sc-29427738-0.sc-67be886a-0.gIUWxk.iTsQBK.sc-2b779603-1.jdlpaE")
      attributes = soup.select("div.Panel--isContentPadded.item--properties > div.sc-29427738-0.sc-67be886a-0.gIUWxk.iTsQBK.sc-2b779603-1.jdlpaE > div.sc-29427738-0.sc-67be886a-1.dVNeWL.emaRpb")
      for each in attributes:
        property_type = each.select("div.Property--type")[0].text
        property_value = each.select("div.Property--value")[0].text
        property_rarity = each.select("div.Property--rarity")[0].text
        
        data_json = {}
        data_json["ape's_name"] = title_name
        data_json["attributes_type"] = property_type
        data_json["attributes_value"] = property_value
        data_json["attributes_rarity"] = property_rarity
        mycollection.insert_one(data_json)


if __name__ == '__main__':
  q2()
  q3()