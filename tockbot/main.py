from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
from reservation import RESERVATION
import time

RESERVATION_HELD = False
WAIT_DELAY = 1000

class TockBot():
  def __init__(self):
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    self.driver = webdriver.Chrome(options=options)
  
  def reserve(self):
    nondate = self.get_nondate()
    self.driver.get('https://www.exploretock.com/%s/search?date=%s&size=%s&time=%s' % (RESERVATION.location, nondate, RESERVATION.size, RESERVATION.start_time.replace(':', '%3A')))
    WebDriverWait(self.driver, WAIT_DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.SearchBarMonths')))
    while not RESERVATION_HELD:
      self.search_dates()
      self.quit()
    time.sleep(600)

  def search_dates(self):
    global RESERVATION_HELD
    days = self.driver.find_elements(By.CSS_SELECTOR, 'button.ConsumerCalendar-day.is-available')
    for day in days:
      aria_label = day.get_attribute("aria-label")
      if aria_label in RESERVATION.dates:
        print(aria_label)
    
    RESERVATION_HELD = True
  
  def get_nondate(self):
    first_date_time = datetime.strptime(RESERVATION.dates[0],'%Y-%m-%d')
    last_date_time = datetime.strptime(RESERVATION.dates[-1],'%Y-%m-%d')
    first_of_month = datetime(first_date_time.year, first_date_time.month, 1).strftime('%Y-%m-%d')
    if first_of_month not in RESERVATION.dates:
      return first_of_month
    else:
      return (last_date_time + timedelta(days=1)).strftime('%Y-%m-%d')

  def quit(self):
    self.driver.quit()

def run_attempt():
  print('Starting reservation attempt for %s for the following days: %s in the month of %s.' % (RESERVATION.location, (', ').join(RESERVATION.days), RESERVATION.month))
  tock_bot = TockBot()
  tock_bot.reserve()
  tock_bot.quit()

run_attempt()
