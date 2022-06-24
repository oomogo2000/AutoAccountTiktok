# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# import undetected_chromedriver as uc
# import csv
# import os



# def main():
#     f = open(os.getcwd()+"/emailList.csv", 'w')
#     writer = csv.writer(f)
#     browser = uc.Chrome()
#     browser.delete_all_cookies()
#     browser.get("https://lastmx.com/")
	
# TODO: tạo địa chỉ mới và chờ

#     for i in range(10):
#         browser.find_element(By.ID, "email").send_keys("")
#         browser.implicitly_wait(2)
#         browser.find_element(By.XPATH, "/html/body/div/div[1]/main/div[1]/div/div/form/div/div/div[1]/div/button").click()
#         time.sleep(10)
#         emailAlias = browser.find_element(By.CLASS_NAME, "form-control").text
#         writer.writerow(emailAlias)
#         browser.refresh()
#         browser.implicitly_wait(2)
#     f.close()

# if __name__ == "__main__":
#     main()