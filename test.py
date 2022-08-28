import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox, simpledialog
import json
import time

class LoginUniandes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path= './drivers/chromedriver')
        self.driver.get('https://login.ezproxy.uniandes.edu.co/login?qurl=http://www.ebooks7-24.com%2f%3fil%3d9168')
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_disable_js(self):
        self.driver.execute_script('''window.open("chrome://settings/content/javascript?search=javascript","_blank");''')
        time.sleep(100)

if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes', report_name='reporte_prueba'))
    #unittest.main()
