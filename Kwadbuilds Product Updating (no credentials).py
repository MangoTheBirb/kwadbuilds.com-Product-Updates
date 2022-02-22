import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Selenium stuff
PATH = ""	# Add chromedriver location
driver = webdriver.Chrome(PATH)

# gspread credentials
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("", scope)	# Add spreadsheet json file
client = gspread.authorize(creds)

# Number of sheets on the google sheets
number_sheets = len(client.open("").worksheets())	# Use spreadsheet name with .open()

delay = 1.5 # Delay of webdriver waits

def Airblade(link, row):
	# Check if cell is empty
	if link is None:
		return None
	
	driver.get(link)

	# Gather Price
	try:
		price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='price--main']//span[@class='money']")))
		price = price_find.text
	except:
		# If price not found, check if the product is not available
		try:
			# Check if the page is not available
			page_not_found = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'fourohfour-title')))
			return None
		except:
			# Otherwise check for the price again
			driver.refresh()
			price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='price--main']//span[@class='money']")))
			price = price_find.text

	# Gather status
	try:
		# Check if it is sold out
		out_of_stock = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'badge--soldout')))
		status = "Out Of Stock"
	except:
		# Otherwise it's in stock
		status = "In Stock"

	# Update cells
	price = price.replace("USD $", "")
	sheet.update_cell(row, 9, price)
	sheet.update_cell(row, 13, status)


def Banggood(link, row):
	# Check if cell is empty
	if link is None:
		return None
	
	driver.get(link)

	# Gather Price
	try:
		# First try getting price
		price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "main-price")))
		price = price_find.text
	except:
		# If price not found, check if the product is not available
		try:
			# Check if the page is not available (with two possible class names)
			try:
				page_not_found = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'stop-text')))
				return None
			except:
				page_not_found = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'stop-text')))
				return None
		except:
			# Otherwise check for the price again
			driver.refresh()
			price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "main-price")))
			price = price_find.text

	# Gather status
	try:
		# Check if it is sold out
		out_of_stock = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'badge--soldout')))
		status = "Out Of Stock"
	except:
		# Otherwise it's in stock
		status = "In Stock"

	# Update cells
	price = price.replace("US$", "")
	sheet.update_cell(row, 10, price)
	sheet.update_cell(row, 14, status)

def GetFPV(link, row):
	# Check if cell is empty
	if link is None:
		return None
	
	driver.get(link)
	
	# Gather Price
	try:
		price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='price-info']//span[@class='price']")))
		price = price_find.text
	except:
		# If price not found, check if the product is not available
		try:
			# Check if the page is not available
			#page_not_found = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'fourohfour-title')))
			#return None
			# I couldn't find an example of a non-available page, so I will just have to wait until there is an error in the program from one to get the web elements
			pass
		except:
			# Otherwise check for the price again
			driver.refresh()
			price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='price-info']//span[@class='price']")))
			price = price_find.text

	# Gather status
	try:
		# Check if it is sold out or if there are multiple options
		try:
			price_label = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'price-label')))
			if (price_label.text == "As low as:"):
				status = "Multiple Options"
			else:
				pass
		except:
			out_of_stock = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'div_availability')))
			status = out_of_stock.text
	except:
		# Otherwise it's in stock
		status = "In Stock"

	# Update cells
	price = price.replace("$", "")
	sheet.update_cell(row, 11, price)
	sheet.update_cell(row, 15, status)

def Rotor_Riot(link, row):
	# Check if cell is empty
	if link is None:
		return None
	
	driver.get(link)
	
	# Gather Price
	try:
		try:
			# Additional Try-Except because elements are different when item is on sale
			price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='product-form__info-list']//span[@class='price']")))
			price = price_find.text
		except:
			price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='product-form__info-list']//span[@class='price price--highlight']")))
			price = price_find.text
	except:
		# If price not found, check if the product is not available
		try:
			# Check if the page is not available
			page_not_found = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'empty-state')))
			return None
		except:
			# Otherwise check for the price again
			driver.refresh()
			price_find = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='product-form__info-list']//span[@class='price']")))
			price = price_find.text
	
	# Gather status
	try:
		# Check if it is sold out or has another status
		price_label = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-form__inventory')))
		if (price_label.text == "Out of stock"):
			status = "Out Of Stock"
		else:
			status = out_of_stock.text
	except:
		# Otherwise it's in stock
		status = "In Stock"
	
	# Update cells
	price = price.replace("$", "")
	sheet.update_cell(row, 12, price)
	sheet.update_cell(row, 16, status)


# Looping through every sheet
for i in range(1, number_sheets-1):		# number_sheets -1 because .worksheets() counts starting at 1
	sheet = client.open("kwadbuildsdb").get_worksheet(i)
	sheet_length = len(sheet.col_values(1))
	# Go to the proper row with gspread
	for j in range(1, sheet_length+1):
		# Run each retailer's function with corresponding link value
		Airblade(sheet.cell(j, 5).value, j)
		Banggood(sheet.cell(j, 6).value, j)
		GetFPV(sheet.cell(j, 7).value, j)
		Rotor_Riot(sheet.cell(j, 8).value, j)