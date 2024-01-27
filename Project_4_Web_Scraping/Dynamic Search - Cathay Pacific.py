# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 14:10:19 2022

@author: Sibo Ding
"""

'''
References about XPath:
https://medium.com/pythoneers/web-scraping-using-selenium-python-6c511258ab50
https://www.guru99.com/xpath-selenium.html
https://devhints.io/xpath
https://www.w3schools.com/xml/xpath_syntax.asp
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def search(dict_search_criteria):
    # Clean the original content
    browser.find_element_by_xpath('//input[@placeholder="Select a departure city"]') \
        .clear()
    # Input origin
    browser.find_element_by_xpath('//input[@placeholder="Select a departure city"]') \
        .send_keys(dict_search_criteria['Origin'])
    time.sleep(1)
    # Click "Enter"
    browser.find_element_by_xpath('//input[@placeholder="Select a departure city"]') \
        .send_keys(Keys.ENTER)
    
    # Input destination
    browser.find_element_by_xpath('//input[@placeholder="Select a destination"]') \
        .send_keys(dict_search_criteria['Destination'])
    time.sleep(1)
    # Click "Enter"
    browser.find_element_by_xpath('//input[@placeholder="Select a destination"]') \
        .send_keys(Keys.ENTER)
    
    
    # Click "Trip type" menu
    browser.find_element_by_class_name('bookTripPanel__tripType').click()
    time.sleep(3)
    if dict_search_criteria['Trip type'] == 'Return':
        browser.find_element_by_id('trip-type-option-R').click()
    elif dict_search_criteria['Trip type'] == 'One way':
        browser.find_element_by_id('trip-type-option-O').click()
    
    
    # Click "Cabin class and passengers" menu
    browser.find_element_by_class_name('cabinClassContainer').click()
    time.sleep(1)
    # Click Cabin class dropdown
    browser.find_element_by_xpath('//label[@id="cabinClassSelection-label"]').click()
    time.sleep(1)
    i = ['First', 'Business', 'Premium Economy', 'Economy'].index(dict_search_criteria['Cabin class'])
    # Select cabin class
    browser.find_element_by_id(f'dropdown-option-{i}').click()
    time.sleep(3)
    
    # Number of passengers
    # while number of input > number on website, click "+" once
    while dict_search_criteria['Number of adults (12+)'] \
        > int(browser.find_element_by_xpath('//div[contains(text(),"Adults")]/div/div[2]').text):
        browser.find_element_by_xpath('//div[contains(text(),"Adults")]/div/div[3]').click()
        time.sleep(5)
    while dict_search_criteria['Number of children (2 to 11)'] \
        > int(browser.find_element_by_xpath('//div[contains(text(),"Children")]/div/div[2]').text):
        browser.find_element_by_xpath('//div[contains(text(),"Children")]/div/div[3]').click()
        time.sleep(5)
    while dict_search_criteria['Number of infants (under 2)'] \
        > int(browser.find_element_by_xpath('//div[contains(text(),"Infants")]/div/div[2]').text):
        browser.find_element_by_xpath('//div[contains(text(),"Infants")]/div/div[3]').click()
        time.sleep(5)
    # Click "Done" button
    browser.find_element_by_class_name('cabinSelectionButton').click()
    time.sleep(2)
    
    
    # Click "Departing on" menu
    # https://www.youtube.com/watch?v=7k4OfXBv5_s&ab_channel=techsapphire
    browser.find_element_by_id('departing-date-input').click()
    for c in range(12):  # Can select 12 months at most from today
        # Check two "month" headers of calendar
        month1 = browser.find_element_by_xpath('//div[@class="DayPicker-Months"]/div[1]/div[1]').text
        month2 = browser.find_element_by_xpath('//div[@class="DayPicker-Months"]/div[2]/div[1]').text
        if month1 == dict_search_criteria['Departing month'] \
            or month2 == dict_search_criteria['Departing month']:
            # Find date by its unique aria-label
            browser.find_element_by_xpath('//div[@aria-label="{}"]'
                                          .format(dict_search_criteria['Departing date'])).click()
            break
        else:
            # Click arrow button to next month
            browser.find_element_by_class_name('dayPicker__navBtn__next').click()
            time.sleep(1)
    
    if dict_search_criteria['Trip type'] == 'Return':
        for c in range(12):
            month1 = browser.find_element_by_xpath('//div[@class="DayPicker-Months"]/div[1]/div[1]').text
            month2 = browser.find_element_by_xpath('//div[@class="DayPicker-Months"]/div[2]/div[1]').text
            if month1 == dict_search_criteria['Returning month'] \
                or month2 == dict_search_criteria['Returning month']:
                browser.find_element_by_xpath('//div[@aria-label="{}"]'
                                              .format(dict_search_criteria['Returning date'])).click()
                break
            else:
                browser.find_element_by_class_name('dayPicker__navBtn__next').click()
                time.sleep(1)
    # Click "Done" button
    browser.find_element_by_xpath('//div[@class="datePickerFlyout__footer"]/button').click()
    
    # Click "Search flights" button
    browser.find_element_by_xpath('//button[@id="booking-search-btn"]').click()


if __name__ == '__main__':
    # Launch Chrome browser
    my_path = r'D:\HKU\Courses\Finance\FINA2390 Financial Programming and Databases\4 Web Scarping\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=my_path)
    # browser.maximize_window()
    
    # Open the webpage
    url = 'https://www.cathaypacific.com/cx/en_HK.html'
    browser.get(url)
    
    dict_search_criteria = {'Origin': 'HKG', 'Destination': 'PEK',
                            'Trip type': 'Return', 'Cabin class': 'Business',
                            'Number of adults (12+)': 2,
                            'Number of children (2 to 11)': 3,
                            'Number of infants (under 2)': 1,
                            'Departing month': 'January 2023',
                            'Departing date': 'Mon Jan 9, 2023',
                            'Returning month': 'April 2023',
                            'Returning date': 'Mon Apr 24, 2023'}
    search(dict_search_criteria)

'''
The rule to fill search criteria:
Origin and Destination: Input 2 IATA 3-letter codes
Trip type: Select 1 item from 'Return' or 'One way'
Cabin class: Select 1 item from 'First', 'Business', 'Premium Economy', 'Economy'
Number of passengers: Input 3 natural numbers
    Maximum sum is 9, at least one adult, num of infants cannot exceed num of adults.
Departing month: Follow the format of 'January 2023'
Departing date: Follow the format of 'Sun Jan 1, 2023'
Returning month: Follow the format of departing. If trip type is 'one way', input ''.
E.g. {'Origin': 'HKG', 'Destination': 'PEK',
      'Trip type': 'Return', 'Cabin class': 'Business',
      'Number of adults (12+)': 2,
      'Number of children (2 to 11)': 3,
      'Number of infants (under 2)': 1,
      'Departing month': 'January 2023', 'Departing date': 'Mon Jan 9, 2023',
      'Returning month': 'April 2023', 'Returning date': 'Mon Apr 24, 2023'}
'''
