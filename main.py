import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver


class LoginUniandes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='./driver/chromedriver')
        self.driver.get('https://www.uniandes.edu.co/')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_login(self):
        self.driver.find_element_by_id('login').click()



if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes', report_name='reporte_prueba'))
    #unittest.main()
