from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import time
from functools import reduce

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def render_page(url):
    chromedriver = "/Applications/chromedriver"
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    driver.quit()
    return r

def scrape_main(page,date):

    url = str(str(page)+str(date))
    r = render_page(url)

    soup = BS(r, "html.parser")
    container = soup.find('lib-city-history-observation')
    table = container.find('tbody')

    main_table_headers = container.find('thead')
    main_table_values = table.find_all('tr', class_='ng-star-inserted')

    return main_table_values

def print_values(data):
    result = []
    for i in data[0]:
        for j in i.find_all('td'):
            result.append(j.text.strip('  '))
    for i, v in enumerate(result):
        print(i, v)

def day_count(data):
    day_counter = 0
    for i in data[1:32]:
        item = i.find('td').text.strip()
        if item.isnumeric():
            day_counter+= 1
        else:
            break
    return day_counter

def create_df(data, date):
    dc = day_count(data)
    result = []
    for i in data:
        for j in i.find_all('td'):
            result.append(j.text.strip('  '))
    month = data[0].find('td').text.strip('  ')

    if dc == 31:
        Day = pd.DataFrame(result[1:32], columns=[month])
        Temp_avg = pd.DataFrame(result[36:128:3], columns = ['Temp_Avg'])
        Dew_point = pd.DataFrame(result[132:224:3], columns = ['Dewpoint_avg'])
        Humidity = pd.DataFrame(result[228:320:3], columns = ['Humidity'])
        wind_speed = pd.DataFrame(result[324:416:3], columns = ['Wind_Speed'])
        Pressure = pd.DataFrame(result[420:512:3], columns = ['Pressure'])
        Rain = pd.DataFrame(result[513:], columns = ['Rain'])
    elif dc == 30:
        Day = pd.DataFrame(result[1:31], columns=[month])
        Temp_avg = pd.DataFrame(result[35:124:3], columns = ['Temp_Avg'])
        Dew_point = pd.DataFrame(result[128:217:3], columns = ['Dewpoint_avg'])
        Humidity = pd.DataFrame(result[221:310:3], columns = ['Humidity'])
        wind_speed = pd.DataFrame(result[314:403:3], columns = ['Wind_Speed'])
        Pressure = pd.DataFrame(result[407:496:3], columns = ['Pressure'])
        Rain = pd.DataFrame(result[497:], columns = ['Rain'])
    elif dc == 29:
        Day = pd.DataFrame(result[1:30], columns=[month])
        Temp_avg = pd.DataFrame(result[34:120:3], columns = ['Temp_Avg'])
        Dew_point = pd.DataFrame(result[124:210:3], columns = ['Dewpoint_avg'])
        Humidity = pd.DataFrame(result[214:300:3], columns = ['Humidity'])
        wind_speed = pd.DataFrame(result[304:390:3], columns = ['Wind_Speed'])
        Pressure = pd.DataFrame(result[394:480:3], columns = ['Pressure'])
        Rain = pd.DataFrame(result[481:], columns = ['Rain'])

    elif dc == 28:
        Day = pd.DataFrame(result[1:29], columns=[month])
        Temp_avg = pd.DataFrame(result[33:116:3], columns = ['Temp_Avg'])
        Dew_point = pd.DataFrame(result[120:203:3], columns = ['Dewpoint_avg'])
        Humidity = pd.DataFrame(result[207:290:3], columns = ['Humidity'])
        wind_speed = pd.DataFrame(result[294:377:3], columns = ['Wind_Speed'])
        Pressure = pd.DataFrame(result[381:464:3], columns = ['Pressure'])
        Rain = pd.DataFrame(result[465:], columns = ['Rain'])

    dfs = [Day, Temp_avg, Dew_point, Humidity, wind_speed, Pressure, Rain]
    df_final = reduce(lambda  left,right: pd.merge(left,right,left_index=True,right_index=True), dfs)
    df_final['Date'] = date + '-' + df_final[month]
    df_final.drop([month], axis = 1, inplace = True)
    return df_final
