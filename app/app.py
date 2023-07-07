from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import base64
import requests
import json
import re

# chromedriver_autoinstaller.install()
app = Flask(__name__)

@app.route('/')
def hello():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # driver = webdriver.Remote('http://selenium:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
    driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options
    )
    driver.get("https://www.google.com/")
    # wait = WebDriverWait(driver, 3600)
    return 'Hello, World!'

@app.route('/test')
def test():
    return 'Hello, World!'

@app.route('/loginLine')
def login():

    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-ssl-errors=yes')
    # options.add_argument('--ignore-certificate-errors')

    # driver = webdriver.Remote('http://selenium:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=options
    )
    # chrome_driver_path = "C:\path\to\chromedriver.exe"

    # options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # service = Service(chrome_driver_path)

    # driver = webdriver.Chrome(service=service, options=options)
    options.add_argument("--incognito")
    # driver.get("https://www.google.com/")
    
    # return 'test'
    driver.get("https://mbasic.facebook.com/")

    driver.get("https://account.line.biz/login?redirectUri=https%3A%2F%2Fmanager.line.biz%2F")
    wait = WebDriverWait(driver, 3600)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    login_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div/form/div/input")
    login_button.click()

    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/div[2]/a')
    login_button.click()

    time.sleep(3)

    qr = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div[2]/div[1]/p/img')

    screenshot = qr.screenshot_as_base64

    base64_encoded_with_scheme = f"data:image/png;base64,{screenshot}"
    print(base64_encoded_with_scheme)

    wait.until(EC.invisibility_of_element_located(qr))

    pin = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div[2]/div[1]/p[1]')
    text_pin = pin.text.strip()

    # response pin
    print(text_pin)
    wait.until(EC.invisibility_of_element_located(pin))
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

@app.route('/loginFB')
def loginFB():
    email = 'taweewong.alongkon@gmail.com'
    pwd = 'AlongTawee09173!'
    code2fa = 'IVTLBSH4QHWYJSB6IAQXJJWTV6LZ553V'
    url = 'https://2fa.live/tok/'+code2fa

    options = webdriver.ChromeOptions()

    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=options
    )
    # chrome_driver_path = "C:\path\to\chromedriver.exe"

    options.add_argument("--headless")

    options.add_argument("--incognito")
    
    driver.get("https://mbasic.facebook.com/")
    wait = WebDriverWait(driver, 3600)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    
    email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    email_input.send_keys(email)

    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='pass']")
    password_input.send_keys(pwd)

    login_button = driver.find_element(By.XPATH, '//*[@id="login_form"]/ul/li[3]/input')
    login_button.click()
    time.sleep(2)

    wait.until(EC.invisibility_of_element_located(login_button))
    time.sleep(3)
    headers = {
        'authority': '2fa.live',
        'accept': '*/*',
        'accept-language': 'th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gcl_au=1.1.750766280.1688013309; _ga_R2SB88WPTD=GS1.1.1688013309.1.0.1688013309.0.0.0; _ga=GA1.2.884927119.1688013309; _gid=GA1.2.1581586134.1688013309; _gat_gtag_UA_78777107_1=1',
        'referer': 'https://2fa.live/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    token = data["token"]

    approvals_input = driver.find_element(By.CSS_SELECTOR, "input[name='approvals_code']")
    approvals_input.send_keys(token)
    approvalsBtn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]')))
    approvalsBtn.click()

    wait.until(EC.invisibility_of_element_located(approvals_input))
    time.sleep(3)
    urlCheckpoint = 'https://mbasic.facebook.com/login/checkpoint/'
    if driver.current_url == urlCheckpoint:
        while driver.current_url == urlCheckpoint:
            try:
                # time.sleep(3)
                element1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]')))
                element1.click()
                time.sleep(3)
            except :
                print("No checkpoint element found.")
                time.sleep(3)

    cookies = driver.get_cookies()
    cookie_raw = ''
    for cookie in cookies:
        cookie_raw = cookie_raw + cookie['name'] + "="+ cookie['value']+ ";"
    print('cookie_raw ',cookie_raw)

    driver.get('https://mbasic.facebook.com/adsmanager/manage/accounts?act')
    time.sleep(5)
    
    # ค้นหา element ที่มีค่า _accessToken
    access_token_element = driver.find_element(By.XPATH, "//script[contains(text(), '_accessToken')]")
    time.sleep(3)
    # ดึงข้อมูลจาก element
    access_token_script = access_token_element.get_attribute('innerHTML')

    # ค้นหาค่า _accessToken โดยใช้ regular expression
    access_token_pattern = r'_accessToken="(\w+)'
    match = re.search(access_token_pattern, access_token_script)

    if match:
        token = match.group(1)
        print(f"Access Token: {token}")
    else:
        print("Access Token not found")

    time.sleep(5)

    driver.get('https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed')

    time.sleep(5)
    # Get the page source
    page_source = driver.page_source
    # Extract the required data using regular expressions
    fb_dtsg = ''
    d = re.search(r'{\\"dtsg\\":{\\"token\\":\\"([^\\]+)', page_source)
    if d:
        regex = re.compile(r'\\"dtsg\\":\{\\"token\\":\\"([^\\]+)\\"')
        matchs = regex.search(page_source)
        fb_dtsg = matchs and matchs.group(1).split(',')[0]
        n = re.search(r'\\"NAME\\":\\"([^"]+)', page_source)
        ids = re.search(r'\\"ACCOUNT_ID\\":\\"([^"]+)', page_source)
        ids = ids.group(1).rstrip('\\').replace('\\\\', '\\')
        name = n.group(1).rstrip('\\').replace('\\\\', '\\')
        __rev = re.search(r'server_revision+\\":+(\d+)', page_source).group(1)

    print('fb_dtsg = ',fb_dtsg)
    time.sleep(2)
    driver.quit()
    result={
        "cookie_raw":cookie_raw,
        "fb_dtsg":fb_dtsg,
        "fb_power_token":token
    }
    return result

@app.route('/loginFBL')
def loginFBL():
    email = 'taweewong.alongkon@gmail.com'
    pwd = 'AlongTawee09173!'
    code2fa = 'IVTLBSH4QHWYJSB6IAQXJJWTV6LZ553V'
    url = 'https://2fa.live/tok/'+code2fa

    chrome_driver_path = "C:\path\to\chromedriver.exe"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--incognito")

    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("https://mbasic.facebook.com/")
    wait = WebDriverWait(driver, 3600)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    
    email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    email_input.send_keys(email)

    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='pass']")
    password_input.send_keys(pwd)

    login_button = driver.find_element(By.XPATH, '//*[@id="login_form"]/ul/li[3]/input')
    login_button.click()
    time.sleep(2)

    wait.until(EC.invisibility_of_element_located(login_button))
    time.sleep(3)
    headers = {
        'authority': '2fa.live',
        'accept': '*/*',
        'accept-language': 'th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gcl_au=1.1.750766280.1688013309; _ga_R2SB88WPTD=GS1.1.1688013309.1.0.1688013309.0.0.0; _ga=GA1.2.884927119.1688013309; _gid=GA1.2.1581586134.1688013309; _gat_gtag_UA_78777107_1=1',
        'referer': 'https://2fa.live/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    token = data["token"]

    approvals_input = driver.find_element(By.CSS_SELECTOR, "input[name='approvals_code']")
    approvals_input.send_keys(token)
    approvalsBtn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]')))
    approvalsBtn.click()

    wait.until(EC.invisibility_of_element_located(approvals_input))
    time.sleep(3)
    urlCheckpoint = 'https://mbasic.facebook.com/login/checkpoint/'
    if driver.current_url == urlCheckpoint:
        while driver.current_url == urlCheckpoint:
            try:
                # time.sleep(3)
                element1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkpointSubmitButton-actual-button"]')))
                element1.click()
                time.sleep(3)
            except :
                print("No checkpoint element found.")
                time.sleep(3)

    cookies = driver.get_cookies()
    cookie_raw = ''
    for cookie in cookies:
        cookie_raw = cookie_raw + cookie['name'] + "="+ cookie['value']+ ";"
    print('cookie_raw ',cookie_raw)

    driver.get('https://mbasic.facebook.com/adsmanager/manage/accounts?act')
    time.sleep(5)
    
    # ค้นหา element ที่มีค่า _accessToken
    access_token_element = driver.find_element(By.XPATH, "//script[contains(text(), '_accessToken')]")
    time.sleep(3)
    # ดึงข้อมูลจาก element
    access_token_script = access_token_element.get_attribute('innerHTML')

    # ค้นหาค่า _accessToken โดยใช้ regular expression
    access_token_pattern = r'_accessToken="(\w+)'
    match = re.search(access_token_pattern, access_token_script)

    if match:
        token = match.group(1)
        print(f"Access Token: {token}")
    else:
        print("Access Token not found")

    time.sleep(5)

    driver.get('https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed')

    time.sleep(5)
    # Get the page source
    page_source = driver.page_source
    # Extract the required data using regular expressions
    fb_dtsg = ''
    d = re.search(r'{\\"dtsg\\":{\\"token\\":\\"([^\\]+)', page_source)
    if d:
        regex = re.compile(r'\\"dtsg\\":\{\\"token\\":\\"([^\\]+)\\"')
        matchs = regex.search(page_source)
        fb_dtsg = matchs and matchs.group(1).split(',')[0]
        n = re.search(r'\\"NAME\\":\\"([^"]+)', page_source)
        ids = re.search(r'\\"ACCOUNT_ID\\":\\"([^"]+)', page_source)
        ids = ids.group(1).rstrip('\\').replace('\\\\', '\\')
        name = n.group(1).rstrip('\\').replace('\\\\', '\\')
        __rev = re.search(r'server_revision+\\":+(\d+)', page_source).group(1)

    print('fb_dtsg = ',fb_dtsg)
    time.sleep(2)
    driver.quit()
    result={
        "cookie_raw":cookie_raw,
        "fb_dtsg":fb_dtsg,
        "fb_power_token":token
    }
    return result


if __name__ == '__main__':
    app.run(debug=True)