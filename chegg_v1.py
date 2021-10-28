from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
from time import sleep
import json

PROXY = "96.9.77.203:55667"
options = Options()
options.add_argument('--user-data-dir=C:/Users/Plex/Desktop/Cheggy/User Data') 
options.add_argument('-profile-directory=Profile 2')
options.add_argument('--disable-gpu')
options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(executable_path="C:/Users/Plex/Desktop/Cheggy/driver/chromedriver.exe", chrome_options=options)


def site_login(driver, answerArr):
    
    #login

    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))

    driver.find_element_by_link_text("Sign in").click()

    data = json.load(open('data.json'))
    
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.NAME, "login")))
    driver.find_element_by_id("emailForSignIn").send_keys(data['email'])
    driver.find_element_by_id ("passwordForSignIn").send_keys(data['password'])
    driver.find_element_by_name("login").click()

    # gets answer after logging in
    get_answers(driver, answerArr)

def get_answers(driver, answerArr):

    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "answer-given-body")))
    answer = driver.find_element_by_class_name("answer-given-body")
    images = answer.find_elements_by_tag_name("img")

    # prints pics answer urls
    for image in images:
        # print(image.get_attribute('src'))
        answerArr.append(image.get_attribute('src'))

    # prints plain text answer
    # print(answer.text)
    answerArr.append(answer.text)

def main(url, answerArr):
    
    #options = Options()
    #options.add_argument('--user-data-dir=C:/Users/Plex/Desktop/Cheggy/User Data') 
    ##changes ur directory
    #options.add_argument('-profile-directory=Profile 2')
    ##options.add_argument("--window-size=0,0")
    ##options.add_argument("--window-position=-10000,0")
    ##options.add_argument("--start-minimized")
    #options.add_argument('--disable-gpu')
    #options.add_argument("--no-sandbox")  
    ##options.add_argument('--headless') 
    ##crashes gpu

    ## links ur own exec path
    #driver = webdriver.Chrome(executable_path="C:/Users/Plex/Desktop/Cheggy/driver/chromedriver.exe", chrome_options=options)
    ##  driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    
    
    # exception handling: determines the need to log in
    try:
        driver.implicitly_wait(2)
        if driver.find_element_by_link_text("Sign in").is_enabled():
            site_login(driver, answerArr)
            #time.sleep(5)
        
    except NoSuchElementException:
        get_answers(driver, answerArr)

    # keeps the browser opened to save login credentials

    driver.quit()
    
    
def site_login():
    
    #login
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))

        driver.find_element_by_link_text("Sign in").click()

        data = json.load(open('data.json'))
    
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.NAME, "login")))
        driver.find_element_by_id("emailForSignIn").send_keys(data['email'])
        driver.find_element_by_id ("passwordForSignIn").send_keys(data['password'])
        driver.find_element_by_name("login").click()
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
    except:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])


def get_answers(URL,answerArr):
    
    
    try:
        driver.get(URL)
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, "answer-given-body")))
        answer = driver.find_element_by_class_name("answer-given-body")
        images = answer.find_elements_by_tag_name("img")

        # prints pics answer urls
        for image in images:
            # print(image.get_attribute('src'))
            answerArr.append(image.get_attribute('src'))

        # prints plain text answer
        # print(answer.text)
        answerArr.append(answer.text)
    
        #element = driver.find_element_by_class_name("desktop")
        #driver.close()
        
        #driver.execute_script("window.open('');")
        #driver.switch_to.window(driver.window_handles[1])
        return answerArr
    except TimeoutException:
        init2CaptchaRequest(URL)
       # get_answers(URL, answerArr)
        sleep(2000)

        
    

def init2CaptchaRequest(site_url):
    API_KEY = "068d837526a4d85cc0eab09ea0c4f917"
    site_key = "6Lcj-R8TAAAAABs3FrRPuQhLMbp5QrHsHufzLf7b"
    url = site_url
    session = requests.Session()
    captcha_id = session.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key, url)).text.split('|')[1]
    print("captcha_id: ", captcha_id)
    print("page url: ", url)
    
    recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    print("token: ", recaptcha_answer)
    print("solving ref captcha...")
    
    while "CAPCHA_NOT_READY" in recaptcha_answer:
        sleep(5)
        recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
        print("token: ", recaptcha_answer)
    
    recaptcha_answer = recaptcha_answer.split('|')[1]
     

    js1 = "document.getElementById('g-recaptcha-response').innerHTML='{}'".format(recaptcha_answer)
    driver.execute_script(js1)
    
    js2 = "handleCaptcha()"
    driver.execute_script(js2)

def openDriver():
    
    driver.get("https://www.chegg.com/study")
    site_login()
 
 
def closeDriver():
    driver.quit()
