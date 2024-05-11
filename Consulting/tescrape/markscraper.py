from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(executable_path=r'C:\Users\nick2\Downloads\chromedriver-win64\chromedriver.exe')
driver.get("https://mycpa.cpa.state.tx.us/coa/")
excommunicado = []

def baby(name):
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "input#entityName.form-control")
    except:
        driver.find_element(By.CSS_SELECTOR, 'a#searchAgainNew.btn.btn-lg.btn-primary.btn-block').click()
        time.sleep(0.5)
        elem = driver.find_element(By.CSS_SELECTOR, "input#entityName.form-control")
    elem.clear()
    elem.send_keys(name)
    print(f'Type {name}')
    time.sleep(.5)
    elem.send_keys(Keys.RETURN)
    print(f'Search {name}')
    time.sleep(1)

    success = len(driver.find_elements(By.CSS_SELECTOR, "div.alert.alert-success")) > 0
    if not success:
        print('success not found')
        check = len(driver.find_elements(By.CSS_SELECTOR, "span.glyphicon.glyphicon-exclamation-sign")) < 1
        if check:
            print('fail not found, clicking search')
            driver.find_element(By.CSS_SELECTOR, 'button#search.btn.btn-lg.btn-primary.btn-block').click()
            time.sleep(1)
            success = len(driver.find_elements(By.CSS_SELECTOR, "div.alert.alert-success")) > 0

    print(success)
    if not success: raise Exception(f'{name} was not picked up by Baby')
    global IN
    IN = True
    # print(f'collecting {name} buttons')
    table = driver.find_element(By.TAG_NAME, "table")
    btns = table.find_elements(By.TAG_NAME, "button")
    print(f'collected {name} buttons: {len(btns)}')
    # print(btns)
    warningText = None
    L = []
    for btn in btns:
        try:
            btn.click()
        except:
            print('/// Missed click, retrying ///')
            time.sleep(.25)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(.5)
            btn.click()
            print('/// success ///')
        time.sleep(.5)
        # skip this button if a warning label is found
        errorMess = driver.find_element(By.CSS_SELECTOR, "span#errorMess").text
        if len(errorMess)>1 and errorMess!=warningText:
            warningText = driver.find_element(By.CSS_SELECTOR, "span#errorMess").text
            print(f'!!! WARNING {warningText} FOUND !!!')
            time.sleep(.25)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(.5)
            continue
        # print(driver.find_element(By.ID, "businessEntityName").text)
        temp = driver.find_elements(By.TAG_NAME, "th")
        NAME = temp[4].text.replace(',','.')
        temp = driver.find_elements(By.TAG_NAME, 'td.text-left')
        ID = temp[0].text.replace(',','.')
        MAIL = temp[1].text.replace(',','.')
        RIGHT = temp[2].text
        if '\n' in RIGHT:
            RIGHT = RIGHT[:RIGHT.index('\n')]
        STATE = temp[3].text.replace(',','.')
        REGISTRATION_DATE = temp[4].text.replace(',','.')
        FILE_NUMBER = temp[5].text.replace(',','.')
        AGENT = temp[6].text.replace(',','.')
        ADDRESS = temp[7].text.replace(',','.')
        # for i in temp: print('|', i.text)
        L.append([AGENT,NAME,ADDRESS,MAIL,RIGHT,STATE,ID,REGISTRATION_DATE,FILE_NUMBER])
        time.sleep(.25)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(.5)
    try:
        driver.find_element(By.CSS_SELECTOR, 'a#searchAgainNew.btn.btn-lg.btn-primary.btn-block').click()
    except:
        print('/// Missed Search Again, retrying')
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, 'a#searchAgainNew.btn.btn-lg.btn-primary.btn-block').click()
        print('/// success ///')
    IN = False
    return L

def drive():
    IN = False
    infile = open(r'C:\Users\nick2\Desktop\infile.csv','r')
    infile.readline()
    infile.readline()
    infile.readline()
    infile.readline()
    outfile = open(r'C:\Users\nick2\Desktop\outfile.csv','a')
    # title row line
    # outfile.write('Registered Agent Name,Name,Address,Mailing Address,Right to Transact Business in Texas,State of Formation,Texas Taxpayer Number,Effective SOS Registration Date,Texas SOS File Number\n')
    for line in infile:
        name = line.split(',')[0]
        # let baby drive each name in file
        try:
            #### TEST  CASE ####
            # L = baby('ALBERT MARTINEZ')
            # print('THRU')
            # print(f'len:{len(L)},  L:{L}')
            # continue
            ####    ####    ####
            L = baby(name)

            # write data results to outfile
            print(f'Writing {len(L)} lines to outfile')
            for LIST in L:
                outfile.write(f'{LIST[0]},{LIST[1]},{LIST[2]},{LIST[3]},{LIST[4]},{LIST[5]},{LIST[6]},{LIST[7]},{LIST[8]}\n')
        except Exception as e:
            if IN: # need to click New Search button to go back a page
                driver.find_element(By.CSS_SELECTOR, 'a#searchAgainNew.btn.btn-lg.btn-primary.btn-block').click()
                time.sleep(1)
            # report missed name
            if ' was not picked up by Baby' in str(e):
                print(f'{str(e)[:-26]} is excommunicado')
                excommunicado.append(str(e)[:-26])
                continue
            if 'target window already closed' not in str(e): # skip window close warnings
                print('///',e,'///')
            # attempt next name
    infile.close()
    outfile.close()

    driver.close()
    print(f'EX: {excommunicado}')

drive()