import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tkinter import messagebox



class LoginUniandes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('https://login.ezproxy.uniandes.edu.co/login?qurl=http://www.ebooks7-24.com%2f%3fil%3d9168')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_login(self):
        self.driver.find_element(By.CSS_SELECTOR, '.centrado1 > a').click()
        # manual login
        messagebox.showinfo('LOGIN', 'Please complete the login form and the 2-step verification process then click OK')

        # read button
        self.driver.find_element(By.XPATH, '//*[@id="button-1056-btnInnerEl"]').click()

        messagebox.showinfo('READ', 'Please click OK to read the book')



if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes', report_name='reporte_prueba'))
    #unittest.main()
