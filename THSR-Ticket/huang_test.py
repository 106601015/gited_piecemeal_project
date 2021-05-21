import requests
from selenium import webdriver
from time import sleep
from PIL import Image

# 開瀏覽器連上高鐵訂票網站，抓驗證圖片存入img_source.png
# 需調整解析度
def get_THSR_verificationCode_photo():
    url = 'http://irs.thsrc.com.tw/IMINT'
    driver = requests.Session()                                                 # 開Session
    option = webdriver.ChromeOptions()                                          # 瀏覽器用Chrome
    option.add_experimental_option('excludeSwitches', ['enable-automation'])    # 用開發者模式啟動，webdriver屬性用正常值
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    sleep(3)                                                                    # 這邊等他三秒跑完loading再視窗最大化+同意
    #driver.maximize_window()                                                    # 視窗最大化
    driver.find_element_by_id('btn-confirm').click()                            # 我同意啦哪次不同意

    driver.save_screenshot('img_screenshot.png')                                # 訂票畫面螢幕截圖
    element = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')   # 找verificationCode圖片元素的位置
    x_bia, y_bia = 140, 140
    left = element.location['x'] + x_bia
    right = element.location['x'] + element.size['width'] + x_bia
    top = element.location['y'] + y_bia
    bottom = element.location['y'] + element.size['height'] + y_bia
    print('---> left, top, right, bottom:', left, top, right, bottom)

    img = Image.open('img_screenshot.png')
    img2 = img.crop((left, top, right, bottom))
    img2.save('img_source.png')

    sleep(10)
    return driver

# 輸入資料
def inputdata(driver):
    driver.find_element_by_xpath("//option[@value='4']").click()
    driver.find_element_by_xpath("(//option[@value='12'])[2]").click()
    # 起點終點
    # 1南港2台北4桃園7台中11台南12左營

    driver.find_element_by_id("trainCon:trainRadioGroup_0").click()
    # 車廂種類
    # "trainCon:trainRadioGroup_0" 標準
    # "trainCon:trainRadioGroup_1" 商務

    sleep(0.5)
    driver.find_element_by_id("seatRadio0").click()
    # 座位喜好
    # "seatRadio0" 無
    # "seatRadio1" 靠窗優先
    # "seatRadio2" 走道優先

    driver.find_element_by_id("ToTimePicker").click()  # 點去程日曆
    driver.find_element_by_xpath("//tr[6]/td[5]").click() # 輸入日期
    # 在2021年5月13日用，//tr[6]/td[5]對應 6/3日期
    # 這邊每次都要用<//tr[?]/td[?]>查日期確認
    driver.find_element_by_id("toTimeInputField").click() # 點去程日期輸入

    driver.find_element_by_name("toTimeTable").click()  # 點去程時間
    driver.find_element_by_xpath("//option[@value='1100A']").click()
    # value填：530A=早上5:30，1130A=早上11:30，1200N=中午12:00，1130P=晚上11:30

    driver.find_element_by_name("ticketPanel:rows:4:ticketAmount").click()
    # 票種
    # "ticketPanel:rows:0:ticketAmount" 全票
    # "ticketPanel:rows:1:ticketAmount" 孩童票6-11
    # "ticketPanel:rows:2:ticketAmount" 愛心票
    # "ticketPanel:rows:3:ticketAmount" 敬老票>65
    # "ticketPanel:rows:4:ticketAmount" 大學生優惠票
    driver.find_element_by_xpath("//option[@value='1F']").click()
    # 票數
    # 3位就3F

    sleep(5)
    ######################################################

    result = input('輸入驗證碼：')
    driver.find_element_by_name("homeCaptcha:securityCode").clear()
    driver.find_element_by_name("homeCaptcha:securityCode").send_keys(result)   # 輸入驗證碼
    driver.find_element_by_id("SubmitButton").click()                           # 開始查詢
    try:
        if driver.find_element_by_class_name("section_title").text != "":       # 有訂位明細
            login_sucess=True
        else:
            login_sucess=False
            print("登錄失敗!")
    except:
        print("驗證失敗! (except)")

    print('login_sucess:', login_sucess)
    return login_sucess



if __name__ == '__main__':
    driver = get_THSR_verificationCode_photo()                                  # 取得driver跟驗證碼圖片
    sleep(2)
    login_sucess = inputdata(driver)                                            # 輸入資料
    if login_sucess == False:
        print("關閉瀏覽器")
        driver.quit()