from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from datetime import datetime

RES_LOCATION = 'quintonil'
RES_DATES = ['2024-05-08', '2024-05-09', '2024-05-10']
START_TIME = '18:00'
END_TIME = '20:00'
RES_SIZE = 4
RES_FOUND = False

class TockBot():
  def __init__(self):
    options = Options()
    options.add_experimental_option('detach', True)
    self.driver = webdriver.Chrome(options=options)
  
  def reserve(self, date):
    print('Starting reservation attempt.')
    self.driver.get('https://www.exploretock.com/%s/search?date=%s&size=%s&time=%s' % (RES_LOCATION, date, RES_SIZE, START_TIME.replace(':', '%3A')))
    try:
      experiences = driver.find_element(By.CLASS_NAME, 'SearchModalExperiences')
    except Exception as e:
      print('No reservations for this date found.')

  def quit(self):
    self.driver.quit()

def run_attempt():
  tock_bot = TockBot()
  tock_bot.reserve(RES_DATES[0])

run_attempt()
