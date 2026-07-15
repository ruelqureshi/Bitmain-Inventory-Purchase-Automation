from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
import lxml, requests, time, sys
import configparser


max_qty = int(sys.argv[1])

config = configparser.ConfigParser()
config.read('settings.ini')

e = str(config['Credentials']['email'])
p = str(config['Credentials']['password'])
api_key = str(config['Credentials']['api_key'])
quantity = str(config['Credentials']['quantity'])
product_id = str(config['Credentials']['product_id'])

if int(quantity) > max_qty:
    quantity = max_qty

# Function declaration
def captcha_solver(img_name, api_key):
    solver = TwoCaptcha(api_key)
    code = solver.normal(img_name)['code']
    return code

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)


stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.maximize_window()
driver.implicitly_wait(25)
driver.get("https://account.bitmain.com/sign_in?method=2&service=https%3A%2F%2Fwww.bitmain.com%2F")

print("[+] Logging in.")
email = driver.find_element('xpath', "//input[@placeholder='Please enter E-mail Address']")
email.send_keys(e)

password = driver.find_element('xpath', "//input[@placeholder='Please enter the password']")
password.send_keys(p)
password.send_keys(Keys.RETURN)

move_slider =  driver.find_element('xpath', "//span[@id='nc_2_n1z']")
move = ActionChains(driver)
move.click_and_hold(move_slider).move_by_offset(500, 0).release().perform()

while True:
    if driver.current_url == 'https://www.bitmain.com/':
        break

driver.get(f"https://order.bitmain.com/user/orderConfirm?productId={product_id}&productCount={quantity}&fittingIds=")

print("[+] Selecting Shipping Method.")
shipping_method = driver.find_element('xpath', "//span[@class='item']")
shipping_method.click()

print("[+] Signing Aggreement.")
aggreement = driver.find_element('xpath', "//span[@class='checkbox']")
aggreement.click()


submit = driver.find_element('xpath', "//button[@class='button ivu-btn']")
submit.click()

def captcha():
	page = driver.page_source
	page = BeautifulSoup(page, 'lxml')
	captcha_img_link = page.findAll('div', {'class':'verification-code'})[1].find('img').attrs['src']


	cookies = driver.get_cookies()
	s = requests.Session()
	for cookie in cookies:
	    s.cookies.set(cookie['name'], cookie['value'])

	response = s.get(captcha_img_link, stream=True)

	with open('img.jpeg', 'wb') as f:
	    f.write(response.content)

while True:
    print("[+] Computing captcha.")
    captcha()
    captcha_answer = captcha_solver('img.jpeg', api_key)
    if '=' in captcha_answer or '?' in captcha_answer:
        captcha_answer = captcha_answer.replace('?', '')
        captcha_answer = captcha_answer.replace('=', '')
        eval(f"{captcha_answer}")
        enter_captcha = driver.find_element('xpath', "//input[@type='text']")
        enter_captcha.send_keys(captcha_answer)
        print(captcha_answer)
        print("[+] Submiting answer.")
        submit_captcha = driver.find_element('xpath', "//button[@class='submit']")
        submit_captcha.click()
    elif 'x' in captcha_answer:
            captcha_answer = captcha_answer.replace('x', '*')
            eval(f"{captcha_answer}")
            enter_captcha = driver.find_element('xpath', "//input[@type='text']")
            enter_captcha.send_keys(captcha_answer)
            print(captcha_answer)
            print("[+] Submiting answer.")
            submit_captcha = driver.find_element('xpath', "//button[@class='submit']")
            submit_captcha.click()
    elif 'Verification failed. The answer you entered is incorrect. Please try again.' in driver.page_source:
        eval(f"{captcha_answer}")
        enter_captcha = driver.find_element('xpath', "//input[@type='text']")
        enter_captcha.send_keys(captcha_answer)
        print(captcha_answer)
        print("[+] Submiting answer.")
        submit_captcha = driver.find_element('xpath', "//button[@class='submit']")
        submit_captcha.click()
    elif 'Order has been placed.' in driver.page_source:
        break
    else:
        eval(f"{captcha_answer}")
        enter_captcha = driver.find_element('xpath', "//input[@type='text']")
        enter_captcha.send_keys(captcha_answer)
        print("[+] Submiting answer.")
        submit_captcha = driver.find_element('xpath', "//button[@class='submit']")
        submit_captcha.click()
        time.sleep(7)

time.sleep(1000)