from selenium import webdriver
import time
import json
import threading
from constants import USERNAME, PASSWORD
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


numberOfConsec = 6      # Number of consecutive
ratio = 1.99            # Trigger ratio. Ex: (Bets below 2.00x.)
basebet = 10            # Your Basebet - gets multiplied afterwards
maxMultiplier = 6
url = "https://www.maxbet.rs/ibet-web-client/#/home/game/spribe/aviator"


def login():
    while(not checkLogin()):
        try:
            driver.switch_to.default_content()
            log_but = driver.find_element_by_xpath('//*[@id="app-loaded"]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/input').click()
            time.sleep(1)   
            mail = driver.find_element_by_xpath('//*[@id="app-loaded"]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/input[1]')
            password = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/input[2]')
            mail.send_keys(USERNAME)
            time.sleep(1)
            password.send_keys(PASSWORD)
            log_but = driver.find_element_by_xpath('//*[@id="app-loaded"]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/input[4]').click()
            time.sleep(10)
            login_flag=checkLogin()
        except:
            print("Login attempt failed. I'm trying again.")
    print("Logging successfuly.")    


def checkLogin():
    driver.switch_to.default_content()
    username = driver.find_elements_by_class_name("profile-and-gifts-wrapper")
    if len(username) > 0 and username[0].text:
        return True
    else: return False


def iframe():
    
    for a in range(10):
        try:
            iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "seven-plugin")))
            driver.switch_to.frame(iframe)
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='button-block'])//div/div")))
            button.click()
            return None
        except Exception as e:
            print("iframe - Exception: " + str(e))



def get_blocks():
    rates = []
    counter = 0
    while(len(rates) == 0 and counter < 50):
        counter += 1
        try:
            blocks = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "(//div[@class='payouts-block'])[1]//app-bubble-multiplier/div")))
            for block in blocks:
                if block.text != '':
                    rates.append(float(block.text.replace('x','')))
            if(len(rates) != 0):
                return rates
        except Exception as e:
            print("Exception: %s" + str(e))
            pass


def checkTrigger(rates, ratio):
    
    string = "".join(["Y" if rate <= ratio else "N" for rate in rates])
    counter = 0
    for i in string:
        if i == "Y":
            counter += 1
        else: break
    return counter


def getlastscore():
    try:
        block = WebDriverWait(driver, timer).until(EC.presence_of_all_elements_located(By.XPATH, ""))
        element = driver.find_element_by_xpath("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-bubble-multiplier[0]/div")
        return element.text
    except Exception as e:
        print("Exception: " + str(e))


def setupbetting():
    finished = True

    for a in range(50): 
        try: 
            print("Setting Up Bets")
            time.sleep(0.5)
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[2]")))
            button.click()
            time.sleep(0.5)
            
            # /html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[2]
            print("1")
            bet_input = driver.find_element_by_xpath("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input")
            for a in range(6):
                bet_input.send_keys(Keys.BACKSPACE)
                time.sleep(0.2)
            bet_input.send_keys(str(basebet))
            print("2")
            # /html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input
            time.sleep(0.5)
            switch_input = driver.find_element_by_xpath("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[1]/app-ui-switcher/div").click()
            # /html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[1]/app-ui-switcher/div
            time.sleep(0.5)
            print("3")
            limit_input = driver.find_element_by_xpath("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[2]/div/app-spinner/div/div[2]/input")
            for b in range(4):
                limit_input.send_keys(Keys.BACK_SPACE)
                time.sleep(0.2)
            limit_input.send_keys(str(ratio))

            print("finished Bet setup")
            return None
        except Exception as e: 
            print("Bet Setup - Exception: " + str(e))


def placebet(value) -> bool:
    try:
        print("Placing Bet for: " + str(value))

        bet_input = driver.find_element_by_xpath("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input")
        for a in range(6):
            bet_input.send_keys(Keys.BACKSPACE)
            time.sleep(0.1)
        bet_input.send_keys(str(value))
   
        time.sleep(0.2)

        place_input = driver.find_element_by_xpath("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button").click()

        time.sleep(0.2)

        print("Bet placed")

        return True
    except Exception as e:
        print("Placing Bet - Exception: " + str(e))
        return False
    

def saveScore(value: float):
    with open('data.json') as data_file:
        data_loaded = json.load(data_file)
    data_loaded['bets'].append(value)
    with open('data.json', 'w') as f:
        json.dump(data_loaded, f, ensure_ascii=False)
    return None


def tryclicking():
    for a in range(5):
        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/consent/div/div/a"))).click()
            return None
        except Exception as e:
            print("tryclicking - Exception: " + str(e))


def setup():
    try:
        print("Setting up")
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        global driver
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(10)
        driver.maximize_window()
        time.sleep(2)
        tryclicking()
        time.sleep(2)
        login()
        time.sleep(1)
        iframe()
        time.sleep(1)
        setupbetting()
    except Exception as e:
        print("Setting up - Exception - " + str(e))

    return None


def main():
    print("Starting Aviator Tracker Bot..")

    setup()

    old_rates = []
    betting = False
    bettingCounter = 0

    recentScore = get_blocks()

    while running:
        try:
            if checkLogin():
                iframe()
                rates = get_blocks()
                if old_rates[:5] != rates[:5]:
                    # print(f"Last {len(rates)} round: " +  ", ".join([f"{rate}x" for rate in rates ]))
                    try:
                        recentScore.insert(0, float(rates[0]))
                        print(recentScore)
                        if len(recentScore) > 25:
                            recentScore.pop()
                        saveScore(float(rates[0]))
                    except Exception as e:
                        print("Saving Problem " + str(e))
                    count = checkTrigger(recentScore, ratio)

                    if (count % (maxMultiplier + numberOfConsec)) >= numberOfConsec:
                        print(f"!Alert Aviator has {count} blue in a row. Betting now.")
                        betting = True
                    else:
                        betting = False
                        bettingCounter = 0
                        
                    if betting == True:
                        # if rates[0] <= ratio and bettingCounter < maxMultiplier:
                        bettingCounter += 1
                        bet_value = basebet * (2 ** (bettingCounter-1))
                        placebet(int(bet_value))
                        time.sleep(0.1)
                        try:
                            file_path = 'screenshots/bet_' + str(int(time.time())) + '.png'
                            with open((file_path), 'wb') as file:
                                a = driver.find_element_by_xpath("/html")
                                file.write(a.screenshot_as_png)
                        except Exception as e:
                            print("Screenshot Exception - " + str(e))
                        
                time.sleep(3)
                old_rates = rates
            else:
                driver.close()
                setup()

        except Exception as e:
            print("Exception - " + str(e))
            pass
    driver.close()


if __name__ == '__main__':
    while True:
        global running
        running = True
        x = threading.Thread(target=main)
        x.start()
        time.sleep(3600)
        running = False
        time.sleep(15)
        x.join()
        sender.send_msg("Restarting")
