import booking.constants as const
import os, time
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r'/usr/local/bin', teardown=False): #teardown used to determine if we want to kill app after running script
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)

        

    
    
    def land_first_page(self):
        self.get(const.BASE_URL)
    


    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-tooltip-text="Choose your currency"]')
        currency_element.click()
        selected_currecny_element = self.find_element(By.CSS_SELECTOR, f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        selected_currecny_element.click()

    
    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, 'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]')
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        '''This method enables the ability to select dates in the current month as well as dates in the future.
        The calendar only shows the current month and the next month. If a check-in/check-out date is 6 months ahead 
        in the future is passed the bot is unable to select it without first changing the month by clicking 
        the arrow on the calendar.
        
        The equation is number of arrow clicks = (Check-in/Check-out date - Today's Date - Clicks Already Made - 1)
        Equation simplified: num_clicks = (Date Months Away - Clicks Already Made - 1)
        The number of clicks needed to see the next month for all months after the current month is 1.
        If the current date is in April and the given check-in date is in April no clicks are needed. (current month and next month are shown by default)
        If the current date is in April and the given check-in date is in May no clicks are needed. (current month and next month are shown by default)
        If the current date is in April and the given check-in date is in June 1 click is needed.
        If the current date is in April and the given check-in date is in July 2 click are needed.
        If the current date is in April and the given check-in date is in August 3 clicks are needed.
        As you can see everytime you increment the month (for all months greater than current and immediate next month)
        you have to make one more click.
        
        Example:
            Todays Date: 4/25/22
            Check-in: 6/1/22
            num_clicks = 2 Months Away - 0 Clicks Already Made - 1, 1 click needed to see the month of June.
        
        When a check-in date is chosen the calendar does not reset. To determine how many clicks are needed to get
        the correct month for a check-out date from the current position you subtract the number of clicks already made.
        
        Using the above example...
            Today's Date: 4/25/22
            Check-in: 6/1/22
            Check-out: 12/31/22
            num_clicks = 8 Months Away - 1 click already made to get to June - 1, 6 clicks needed to see month of December.'''

        today = datetime.now()
        check_in_dt_obj = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_out_dt_obj = datetime.strptime(check_out_date, '%Y-%m-%d')
        check_in_months_away = (check_in_dt_obj.year - today.year) * 12 + (check_in_dt_obj.month - today.month)
        check_out_months_away = (check_out_dt_obj.year - today.year) * 12 + (check_out_dt_obj.month - today.month)

        
        arrow_element = self.find_element(By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]')
                
        
        # if the given date is in the current or immediate next month no need to change the calendar and select the date 
        if check_in_months_away <= 1:
            check_in_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in_date}"]')
            check_in_element.click()
            check_out_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out_date}"]')
            check_out_element.click()
        
        # else if the given date is outside of current or immidate month
        # determine number of clicks needed to show the correct month to select from the calendar
        # keep track of how many clicks have been made to get the correct month for a check-out date
        elif check_in_months_away > 1:
            clicks_made_so_far = 0
            num_clicks = check_in_months_away - 1
            for i in range(num_clicks):
                arrow_element.click()
                clicks_made_so_far +=1
            check_in_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in_date}"]')
            check_in_element.click()

            num_clicks = check_out_months_away - clicks_made_so_far - 1
            for i in range(num_clicks):
                arrow_element.click()
            check_out_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out_date}"]')
            check_out_element.click()
        
    def select_adults(self, num_adults=1):
        selection_element = self.find_element(By.ID, 'xp__guests__toggle')
        selection_element.click()
        add_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')
        subtract_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
        adult_count_element = self.find_element(By.CSS_SELECTOR, 'span[data-bui-ref="input-stepper-value"]')
        current_adult_count = int(adult_count_element.get_attribute('innerText'))
        for i in range(current_adult_count):
            subtract_element.click()
        
         # subtracting 1 because adult count can only go down to 1
         # if the adult count is 1 1-1=0 and the for loop will not run which is correct
        for i in range(num_adults-1):
            add_element.click()


    def submit(self):
        submit_button = self.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()



    def __exit__(self, *args): #context manager, runs once main.py exits with block
        if self.teardown:
            print('quiting in 5...')
            time.sleep(1)
            print('4')
            time.sleep(1)
            print('3')
            time.sleep(1)
            print('2')
            time.sleep(1)
            print('1')
            time.sleep(1)
            self.quit()
