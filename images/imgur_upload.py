from authenticate import authenticate
from datetime import datetime
import cv2
import matplotlib.pyplot as plt
import urllib
import base64
import json
from imgurpython import ImgurClient
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def main():
    cap = cv2.VideoCapture(2)

    if cap.isOpened():
        ret, frame = cap.read()
        print(ret)
        print(frame)
    else:
        ret = False

    img1 = cv2.imread(frame, cv2.COLOR_BGR2RGB)

    cap.release()

    cv2.imwrite('image.png',img1)

def authenticate():
    config = configparser.ConfigParser()
    config.read('authenticate.ini')

    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')

    imgur_username = config.get('credentials', 'imgur_username')
    imgur_password = config.get('credentials', 'imgur_password')

    client = ImgurClient(client_id, client_secret)

    authorization_url = client.get_auth_url('pin')

    driver = webdriver.Chrome()
    driver.get(authorization_url)

    username = driver.find_element_by_xpath('//*[@id="username"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.clear()
    username.send_keys(imgur_username)
    password.send_keys(imgur_password)

    driver.find_element_by_name("allow").click()

    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.ID, 'pin'))
        WebDriverWait(driver, timeout).until(element_present)
        pin_element = driver.find_element_by_id('pin')
        pin = pin_element.get_attribute("value")
    except TimeoutException:
        print("Timed out waiting for page to load")
    driver.close()

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
    print("Authentication successful!")


    return client


album = None
image_path ='image.png'

def upload_image(client):
    config = {
        'album' : album,
        'name' : 'Box Interior',
        'description' : 'For security stuff: {0}'.format(datetime.now())
    }

    print('Uploading image...')
    image = client.upload_from_path(image_path, config = config, anon = False)
    print("Done!")
    print()

    return image

def inbox_image():
    main()
    client = authenticate()
    image = upload_image(client)
    
    return format(image['link'])
