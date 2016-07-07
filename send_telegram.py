# coding: utf-8

import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import config


__author__ = 'szypulka'


# Define the correct driver
if 'linux' in sys.platform:
    browser = webdriver.Chrome(config.linux_webdriver_path)
    phone = config.phone1
else:
    browser = webdriver.Chrome(config.other_platform_webdriver_path)
    phone = config.phone2


# Fill in telegram fields
browser.get('{}/messages/new'.format(config.test_url))
telegram_data = {
    'message_city': u'Кронштадт',
    'message_region': u'Ленинградской',
    'message_street': u'Ленина',
    'message_house': '2',
    'message_apart': '1',
    'message_recipient': u'Лихолетов Витамин Шэмрокович',
    'message_body': u'Шлите еды поскорее',
    'anonymous_full_name': u'Лихолетов Вейдер Иннотекович',
    'anonymous_phone': phone,
    'anonymous_address': u'Санкт-Петербург Невский 120 2 15'
}

for key in telegram_data:
    browser.find_element_by_id(key).send_keys(telegram_data[key])

browser.find_element_by_name('commit').click()


# Confirm by SMS-code input
for handle in browser.window_handles:
    browser.switch_to.window(handle)
sms_code = str(input('Please input the code\n'))
browser.find_element_by_id('anonymous_token').send_keys(sms_code)
browser.find_element_by_xpath('//button[@type="submit"]').click()


# Select provider and add money
for handle in browser.window_handles:
    browser.switch_to.window(handle)
    time.sleep(1)
browser.find_element_by_xpath("//input[@name='commit']").click()


# Add card details and retrieve money
for handle in browser.window_handles:
    browser.switch_to.window(handle)
card_data = {
    'iPAN_sub': '4111 1111 1111 1111',
    'month': '12',
    'year': '2019',
    'iTEXT': 'PEDRO CAVA',
    'iCVC': '123',
    'email': 'a@a.ru'
}
for key in card_data:
    browser.find_element_by_id(key).send_keys(card_data[key])
browser.find_element_by_id('buttonPayment').click()

# 3D VISA Security
for handle in browser.window_handles:
    browser.switch_to.window(handle)
element = WebDriverWait(browser, 10).until(
    ec.presence_of_element_located((By.NAME, 'password'))
)
element.send_keys('12345678')
browser.find_element_by_xpath('//input[@type="submit"]').submit()

# Confirm sending
for handle in browser.window_handles:
    browser.switch_to.window(handle)
browser.find_element_by_class_name('btn-white').click()

# Check that telegram is sent
for handle in browser.window_handles:
    browser.switch_to.window(handle)
assert u'Телеграмма подготовлена к отправке' in browser.page_source
