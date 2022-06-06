from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#used to seperate code output from file path for easier debugging 
def clean_terminal():
    print('>>>')
    print('>>>')
    print('>>> Starting Program...')
    print('>>>')
    print('>>>')
clean_terminal()

# TODO: Create a driver variable to reference a chrome driver object
driver = webdriver.Chrome()

# TODO: Create a website variable to hold the url to website
website = r'https://demo.seleniumeasy.com/jquery-download-progress-bar-demo.html'

# TODO: determine the html element you want to interact with
# download button

# TODO: determine what attribute of the button html element you can use to identify it
#ID

# TODO: determine the value of the attribute is
#downloadButton

# TODO: Create an element variable to hold the attribute type, attribute value, and find by method associated with the html element
button = {'att_type' : 'ID', 
          'att_value' : 'downloadButton',
          'find_by' : By.ID
          }
progess = {'att_type' : 'class', 
          'att_value' : 'progress-label',
          'find_by' : By.CLASS_NAME
          }



# TODO: Create an element variable to hold values associated with the complete text
# TODO: Store element values for download button in variable
# TODO: Store element values for complete text in variable
# TODO: Open Browser/go to url
driver.get(website)

# TODO: Wait for page to load
driver.implicitly_wait(10) #waits for a max of 10 secs for page to load but won't wait the full 10 if loads before then
# will be the same duration for all elements you are looking for in the program

# TODO: Find button element using find_by, and attribute value and store element in a variable
element = driver.find_element(button['find_by'], button['att_value'])
print('found element')
# TODO: Click button element
element.click()
# TODO: Find complete element
element = driver.find_element(button['find_by'], button['att_value'])
# TODO: Read if element is complete
    #If complete done
    #If not go back to 12 and check again


#explicit wait
WebDriverWait(driver, 30).until(
    EC.text_to_be_present_in_element(
        (By.CLASS_NAME,'progress-label'), #element looking in
        'Complete!' #epected text
    )
)
