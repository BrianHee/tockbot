from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
from reservation import RESERVATION
import time

RESERVATION_HELD = False
REFRESH_DELAY = 1
WAIT_DELAY = 1000
FORMAT_YMD = '%Y-%m-%d'
FORMAT_IMP = '%I:%M %p'

class TockBot():
  def __init__(self):
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    self.driver = webdriver.Chrome(options=options)
  
  def reserve(self):
    nondate = self.get_nondate()
    start_time = datetime.strptime(RESERVATION.start_time, FORMAT_IMP).strftime('%H:%M')
    while not RESERVATION_HELD:
      time.sleep(REFRESH_DELAY)
      self.driver.get('https://www.exploretock.com/%s/search?date=%s&size=%s&time=%s' % (RESERVATION.location, nondate, RESERVATION.size, start_time))
      WebDriverWait(self.driver, WAIT_DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.SearchBarMonths')))
      self.search_dates()
    time.sleep(600)

  def search_dates(self):
    month = self.driver.find_element(By.CSS_SELECTOR, 'div.ConsumerCalendar-month')
    days = month.find_elements(By.CSS_SELECTOR, 'button.ConsumerCalendar-day.is-available')
    if not days:
      print('No available dates found for this month yet.')
      return
    for day in days:
      aria_label = day.get_attribute("aria-label")
      if aria_label in RESERVATION.dates:
        print(f'Availabilities for {aria_label} found - checking times.')
        day.click()
        if self.search_times():
          break
        else:
          print(f'No time available for {aria_label}.')
  
  def search_times(self):
    global RESERVATION_HELD
    experience = self.search_experiences()
    if not experience:
      return False
    for time_slot in experience.find_elements(By.XPATH, "//div[@data-testid='search-result-list-item']"):
      span = time_slot.find_element(By.CSS_SELECTOR, 'span.Consumer-resultsListItemTime').find_element(By.CSS_SELECTOR, 'span')
      date_time = datetime.strptime(span.text, FORMAT_IMP)
      if datetime.strptime(RESERVATION.start_time, FORMAT_IMP) <= date_time <= datetime.strptime(RESERVATION.end_time, FORMAT_IMP):
        print('Time found for: %s. Please complete the reservation.' % (date_time.strftime(FORMAT_IMP)))
        time_slot.click()
        RESERVATION_HELD = True
        return True
    return False

  def search_experiences(self):
    experiences = self.driver.find_elements(By.CSS_SELECTOR, 'button.Consumer-reservationLink')
    if RESERVATION.experience != '':
      for experience in experiences:
        h3 = experience.find_element(By.CSS_SELECTOR, 'h3.Consumer-reservationHeading')
        if h3.text.lower() == RESERVATION.experience.lower():
          return experience
    else:
      return experiences[0]
  
  def get_nondate(self):
    first_date_time = datetime.strptime(RESERVATION.dates[0], FORMAT_YMD)
    first_of_month = datetime(first_date_time.year, first_date_time.month, 1).strftime(FORMAT_YMD)
    if first_of_month not in RESERVATION.dates:
      return first_of_month
    else:
      non_date = first_of_month
      while non_date in RESERVATION.dates:
        non_date = (datetime.strptime(non_date, FORMAT_YMD) + timedelta(days=1)).strftime(FORMAT_YMD)
      return non_date

  def quit(self):
    self.driver.quit()

def run_attempt():
  print('Starting reservation attempt for %s for the following days: %s.' % (RESERVATION.location, (', ').join(RESERVATION.dates)))
  tock_bot = TockBot()
  tock_bot.reserve()
  tock_bot.quit()

run_attempt()
