##### - Skoden's COTP Script

import logging
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime as dt
from datetime import timezone, timedelta
from random import randint
from properties import password 
from properties import countryCode
from properties import phone
from properties import iftttSuccess
from properties import iftttProblem
from properties import dailyProfit
from properties import iftttProfit
from properties import minTimeForProfits
from properties import maxTimeForProfits
from properties import iftttNames
from properties import doReferral
from properties import doCycle
from properties import delayStartTimer
from properties import logLevel
from properties import iftttEnabled
from properties import iftttKeyCode
from properties import headless

import socket

iftttBase = 'https://maker.ifttt.com/trigger/'
iftttMid = '/with/key/'
iftttEnd = '?value1='

class Bot():
    def __init__(self) -> None:

        machineID = socket.gethostname()

        while True:
            try:
                logger = logging.getLogger()
                logger.disabled = True
                logging.info('Initializing ChromeDriver...')
                chrome_options = Options()
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument('--ignore-certificate-errors')
                chrome_options.add_argument('--ignore-ssl-errors')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument("--window-size=1920,1080")

                # go headless (when required)
                headlessBool = str_to_bool(headless)
                if headlessBool == True:
                    chrome_options.add_argument('--headless')
                    logging.info('Enabling headless mode...')
                elif headless == 'Auto' and "IS_DOCKER_CONTAINER" in os.environ:
                    chrome_options.add_argument('--headless')
                    logging.info('Enabling headless mode...')

                self.driver = webdriver.Chrome(options=chrome_options)
                chrome_options.add_argument('--headless')
                self.driver2 = webdriver.Chrome(options=chrome_options)

                try:
                    self.driver2.get('https://docs.google.com/document/d/1QyXvPt1obMeMwYPJ7kdPgHXT3V70OBfT0j03ePYfVZ8/edit?usp=sharing')    #the list of Jamzee licensed members
                    if self.driver2.find_element(By.XPATH, "//*[contains(text(), '" + machineID + "')]"):
                        licensed = True
                        self.driver2.quit()
                    else:
                        logging.info('PC Not licensed')
                        self.driver.quit()
                        self.driver2.quit()
                        os.exit(1)
                except:
                    logging.info('PC Not Registured')
                
                logger.disabled = False
                
                loginSucess = False
                loop = 0
                while loginSucess == False and loop <= 2:
                    try:
                        self.login(countryCode, phone, password)
                        loginSucess = True
                        loop += 1
                        if loginSucess == False:
                            self.driver.close()
                    except:
                        self.driver.close()
                        loginSucess = False
                        loop += 1
                        continue
                if doReferral == True:
                    self.referrals()
                if doCycle == True:    
                    cycled = self.cycleCheck()
            except Exception as e:
                logging.critical('%s', e)
                if iftttEnabled == True:
                    self.driver.get(iftttBase+iftttProblem+iftttMid+iftttKeyCode+iftttEnd+iftttNames)
                sleep(1)
                continue
            
            if cycled == True:
                sleepTime = randint(7300, 7500)
                logging.info('All trades initialized - waiting %s seconds...', sleepTime)
                logging.info('Waiting until %s before trying again...', (dt.datetime.now() + timedelta(seconds=sleepTime)).strftime('%H:%M:%S'))
                if iftttEnabled == True:
                    self.driver.get(iftttBase+iftttSuccess+iftttMid+iftttKeyCode+iftttEnd+iftttNames)
                    sleep(2)
            else:
                sleepTime = randint(30, 120)
                logging.info('Trades not initialized - waiting %s seconds...',sleepTime)
                logging.info('Waiting until %s before trying again...', (dt.datetime.now() + timedelta(seconds=sleepTime)).strftime('%H:%M:%S'))


            self.driver.close()
            sleep(sleepTime)
    
    
    def clickThis(self, xPath):
        clickBtn = None
        loops = 0
        while not clickBtn and loops < 2:
            try:
                clickBtn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, xPath)))
                clickBtn.click()
            except:
                logging.warning("%s not clickable yet - dont worry I'll try again boss", xPath)
                loops +=1

    def login(self, countryCode, phone, password):
        self.driver.get('https://www.cotps.com/#/pages/phonecode/phonecode?from=login')

        try:
            if WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view/uni-input/div/input'))):
                self.driver.find_element(By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view/uni-input/div/input').send_keys(countryCode)
                self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-button')     #Submit Country Code     
                if countryCode == '234':
                    sleep(2)
                    self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-button')     #Submit Country Code 
        except:
            logging.critical('Could not enter Country Code')
            loginSucess = False
                
        try:
            if WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-input/div/input')))   \
                    and WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-input/div/input'))):
                self.driver.find_element(By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-input/div/input').send_keys(phone)      # send Phone Number
                self.driver.find_element(By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-input/div/input').send_keys(password)     # send Password
                sleep(.5)
                self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-button')    # Click Login Button
                self.clickThis('/html/body/uni-app/uni-modal/div[2]/div[3]/div') # Click Pop Up Button
                loginSucess = True
        except:
            logging.critical('Could not enter Phone or Email')
            loginSucess = False                

        return loginSucess

    def referrals(self):
        sleep(1)
        self.driver.get('https://www.cotps.com/#/pages/userCenter/myTeam')   # Open My Team  
        
        try:  
            sleep(2)    
            self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')     # Click Receive
            sleep(2)
        except:
            logging.warning('no referral bonus')

        try:
            sleep(3)
            self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]') #Level 2 Tab click
            sleep(3)
            self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')     # Click Receive
            sleep(3)
        except:
            logging.warning('no level 2 referral bonus')

        try:
            sleep(3)
            self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[3]') #Level 3 Tab click
            sleep(3)
            self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')     # Click Receive
            sleep(3)
        except:
            logging.warning('no level 3 referral bonus')


    def cycleCheck(self):
        self.driver.get('https://www.cotps.com/#/pages/transaction/transaction') # Transaction Hall
        sleep(2)
        tBalance = self.driver.find_element(By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[1]/uni-view[2]').text
        wBalance = self.driver.find_element(By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view[2]').text

        currentTime = dt.datetime.now(timezone.utc).hour
        if minTimeForProfits < currentTime < maxTimeForProfits:
            txThreshold = dailyProfit
        else:
            txThreshold = 5

        if txThreshold < 5:
            txThreshold = 5

        if tBalance == "0.000":
            while float(wBalance) > txThreshold:
                self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button')     # start transaction                
                self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[6]/uni-button[2]')     # Transaction Sell Button
                self.clickThis('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-button')        #Transaction Confirmation Button

                wBalance = self.driver.find_element(By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view[2]').text
            
            if iftttEnabled == True and txThreshold > 5:
                self.driver.get(iftttBase+iftttProfit+iftttMid+iftttKeyCode+iftttEnd+iftttNames)
                sleep(2)
            cycled = True
        else:
            cycled = False
        
        return cycled
       
def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         return False # assume all other values are false

def main():
    while True:
        logging.basicConfig(stream=sys.stdout, level=logLevel)
        logging.info('Waiting %s seconds before starting the script...', delayStartTimer)
        sleep(delayStartTimer)
        my_bot = Bot()
       

if __name__ == '__main__':
    main()