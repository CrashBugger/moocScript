import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains

username = ""
password = ""


def executeJavaScript(driver):
    try:
        script = """Object.defineProperty(navigator,"webdriver",{get: () => false,});"""
        driver.execute_script(script)
    except:
        pass


def initial(beginUrl):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 取消密码弹窗
    prefs = {"": ""}
    prefs["credentials_enable_service"] = False
    prefs["profile.password_manager_enabled"] = False
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.get(url=beginUrl)
    executeJavaScript(driver)
    driver.find_element_by_class_name("ipt-tel").send_keys(username)
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)
    driver.find_element_by_id("loginBtn").click()
    driver.implicitly_wait(10)
    return driver


def operateReStart(driver):
    print("operate restart")
    sleep(2)
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="iframe"]'))
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ext-gen1045"]/iframe'))
    ele = driver.find_element_by_xpath('//*[@id="video"]/div[5]/button[1]')
    ele.click()

def isFinished(driver):
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="iframe"]'))
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ext-gen1045"]/iframe'))
        ele = driver.find_element_by_xpath('//*[@id="video"]/div[5]/button[1]/span[2]')
        if ele.text == '重播':
            return True
        elif ele.text == "播放":
            operateReStart(driver)
            return False
        else:
            return False
    except:
        return True


def clickRight(driver):
    sleep(3)
    driver.switch_to.default_content()
    rights = driver.find_elements_by_class_name("orientationright ")
    if len(rights) > 1:
        for right in rights:
            style = right.get_attribute("style")
            if "block" in style:
                right.click()
                break
    else:
        rights[0].click()
    executeJavaScript(driver)


def judgeEnd():
    try:
        num = urlList[driver.current_url]
        if num > 3:
            print("当前mooc已经刷完")
            driver.close()
            sys.exit(1)
        else:
            urlList[driver.current_url] += 1
    except:
        urlList[driver.current_url] = 1


def slideNextS(driver):
    print("slide")
    sleep(3)
    clickRight(driver)
    judgeEnd()
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="iframe"]'))
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ext-gen1045"]/iframe'))
        driver.find_element_by_class_name('vjs-big-play-button')
        print("slide over")
    except:
        slideNextS(driver)


def operateStart(driver):
    print("operate")
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="iframe"]'))
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ext-gen1045"]/iframe'))
    driver.find_element_by_class_name('vjs-big-play-button').click()
    driver.switch_to.default_content()


if __name__ == '__main__':
    beginUrl = "学习通目标课程url"
    urlList = {}
    urlList[beginUrl] = 1
    driver = initial(beginUrl)
    sleep(2)
    try:
        operateStart(driver)
    except:
        pass
    finally:
        while True:
            sleep(3)
            if isFinished(driver):
                slideNextS(driver)
                operateStart(driver)
