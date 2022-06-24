import os
import datetime
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

import undetected_chromedriver as uc
import json, csv

class My_Chrome():
	def __del__(self):
		pass

	def __init__(self, jsondata, csvdata=[], zoho=False):

		self.csvdata = csvdata
		self.firstName = jsondata["firstName"]
		self.lastName = jsondata["lastName"]
		self.email = jsondata["mainEmail"]
		self.password = jsondata["password"]
		self.logIn = False

		#TODO: tắt cookie SameSite cho lastmx để giải phóng bộ nhớ

		self.browser = uc.Chrome()
		self.browser.delete_all_cookies()
		self.zoho = zoho

	def saveSuccessfulInfo(self, successList):
		f = open(os.getcwd() + "/emailListInformation "+ datetime.date.today() + ".csv", 'w')
		writer = csv.writer(f)
		writer.writerows(successList)
		#tiktok and linked gmail account info
		#tiktok user and password
		#gmail user and password
		f.close()
		return

	def tiktokAccountCreate(self):
		# for i in (0, len(self.csvdata)): 
		self.browser.get("https://www.tiktok.com/signup/phone-or-email/email")
		self.browser.implicitly_wait(10)
		time.sleep(2)
		
		email = self.csvdata[0]
		print(email)

		#TODO: Tạo random password
		# passw = randomPasswordGenerate()
		passw = "Backpack123$" #dummy password

		# check tham số có chính xác không,kiểu boolearn
		e = False
		p = False
		m = False
		d = False
		y = False
		success = False

		while success == False: 
			try: 
				if not e:		
					print("inputting email")				
					WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.NAME, "email")))
					self.browser.find_element(By.NAME, "email").send_keys(email)
					e = True

				if not p:
					print("inputting password")				
					self.browser.find_element(By.CSS_SELECTOR, "input[type = 'password']").send_keys(passw)
					p = True

				if not m:
					month = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Month")]')))
					print("selecting month")
					if month:
						self.browser.find_element(By.XPATH, '//*[contains(text(), "Month")]').click()
						#Random month
						self.browser.find_element(By.XPATH, '//*[contains(text(), "March")]').click()
						m = True
				
				if not d:
					day = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Day")]')))
					print("selecting day")
					if day: 
						self.browser.find_element(By.XPATH, '//*[contains(text(), "Day")]').click()
						self.browser.find_element(By.XPATH, '//*[text() = "31"]').click()
						d = True

				if not y:
					year = WebDriverWait(self.browser, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Year")]')))
					print("selecting year")
					if year:
						self.browser.find_element(By.XPATH, '//*[contains(text(), "Year")]').click()

						#random year selection
						randomInt = random.randint(1980, 2000)
						self.browser.find_element(By.XPATH, '//*[contains(text(), ' + str(randomInt) + ')]').click()
						y = True
				
				success = True
				print("success!")
			except Exception as e: 
				print("error!")
				pass

		self.browser.find_element(By.XPATH, '//button[text() = "Send code"]').click()

		# Lấy 2fa
		tikTokCode = self.getRecentCode(passw)
		print("found code: " + tikTokCode)

		self.browser.close()
		self.browser.switch_to.window(self.browser.window_handles[0])
		self.browser.find_elements(By.XPATH, '//input[@type = "text"]')[1].send_keys(tikTokCode)
		self.browser.find_element(By.CSS_SELECTOR, "button[type = 'submit']").click()

		# self.saveSuccessfulInfo({email, passw})
 
	#Google Signin
	def googleSignIn(self, passw):
		if self.zoho:
			self.zohoSignIn()
			zohoOTPCode = self.zohoSignIn()
					
			self.browser.switch_to.window(self.browser.window_handles[1])

			self.browser.find_element(By.NAME, 'OTP').send_keys(zohoOTPCode)
			self.browser.find_element(By.ID, 'nextbtn').click()

		# self.browser.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin');") 
		# #Bật tab mới
		# self.browser.switch_to.window(self.browser.window_handles[1])
		# crawl các button và ô
		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.XPATH, '//input[@id="identifierId"]')))
		gmailUserBox = self.browser.find_element(By.XPATH, '//input[@id="identifierId"]')
		gmailUserBox.send_keys(self.email)
		gmailUserBox.send_keys(Keys.ENTER)

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.ID, 'identifierId')))
		gmailPasswBox = self.browser.find_element(By.NAME, 'password')
		gmailPasswBox.send_keys(self.password)
		gmailPasswBox.send_keys(Keys.ENTER)
		print("signed into google!")

	#Zoho Signin
	def zohoSignIn(self, email):
		self.browser.execute_script("window.open('https://accounts.zoho.com/signin?servicename=VirtualOffice&signupurl=https://www.zoho.com/mail/zohomail-pricing.html&serviceurl=https://mail.zoho.com', 'zohoSignIN');")
		#Bật tab mới
		self.browser.switch_to.window('zohoSignIN')

		WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.NAME, 'LOGIN_ID')))
		self.browser.find_element(By.NAME, 'LOGIN_ID').send_keys(email)
		self.browser.find_element(By.ID, 'nextbtn').click()   

	# Đợi 2fa gửi về
	def getRecentCode(self, passw):
		self.browser.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin');") 
		#Tiến hành mở tab
		self.browser.switch_to.window(self.browser.window_handles[1])

		if not self.logIn:
			self.googleSignIn(passw)

		print("Please wait a minute before the code is sent to your email")
		# time.sleep(5)
		# self.browser.refresh()

		gmails = self.browser.find_elements(By.XPATH, '//span[@class="bog"]')
		for gmail in gmails:
			if "verification code" in gmail.text:
				return gmail.text[:6]

	def main(self):
		# self.browser.maximize_window()
		self.tiktokAccountCreate()

	
if __name__ == "__main__":

	data = open("settings.json", "r+", encoding="utf8")
	jsondata = json.load(data)
	data.close()
	csvdata = []

	with open(os.getcwd() + '/emailList.csv', mode ='r') as file:
		# Đọc CSV file
		csvFile = csv.reader(file)

		# Hiển thị nội dung CSV file
		for row in csvFile:
			csvdata.append(row)

	newChrome = My_Chrome(jsondata, csvdata)
	newChrome.main()

	hangingStall = input("Hanging")