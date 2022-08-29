import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tkinter import messagebox, simpledialog
import json
import re
import os
import shutil
from sys import platform


if platform == "linux" or platform == "linux2":
    chrome_path = './drivers/chromedriver'

elif platform == "darwin":
    chrome_path = './drivers/chromedriver_mac'

options = Options()
options.add_argument('user-data-dir=/tmp/tarun')




settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings), 'savefile.default_directory': '/home/abel/projects/extract_pdf/pdf/'}
options.add_experimental_option('prefs', prefs)
options.add_argument('--kiosk-printing')
# options.add_argument("--window-size=2000,2000")


# options.add_experimental_option('detach', True)


class LoginUniandes(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path= chrome_path,options=options)
        self.driver.get('https://login.ezproxy.uniandes.edu.co/login?qurl=http://www.ebooks7-24.com%2f%3fil%3d9168')
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_main(self):
        logo = self.driver.find_elements(By.XPATH, '//*[@id="imgLogo"]')

        is_logged = len(logo) > 0

        print('is_logged: ' + str(is_logged))
        messagebox.showinfo('Resultado', 'El usuario está logueado: ' + str(is_logged))

        if is_logged:
            messagebox.showinfo('Login', 'Login exitoso')

        else:
            # manual login
            self.driver.find_element(By.CSS_SELECTOR, '.centrado1 > a').click()
            messagebox.showinfo('LOGIN', 'Please complete the login form and the 2-step verification process then click OK')

        # read button
        self.driver.find_element(By.XPATH, '//*[@id="button-1056-btnInnerEl"]').click()

        # ask for pages range
        first_page = simpledialog.askinteger('FIRST PAGE', 'Enter the first page number')
        last_page = simpledialog.askinteger('LAST PAGE', 'Enter the last page number')
        if first_page is None or first_page == '':
            first_page = 1
        if last_page is None or last_page == '':
            last_page = 702

        # select pages range

        self.assertGreater(last_page, first_page)
        self.assertGreater(last_page, 0)
        self.assertLessEqual(last_page, 702)


        input_page = self.driver.find_element(By.XPATH, '//*[@id="VIEWER_page9168-inputEl"]')
        input_page.clear()
        input_page.send_keys(str(first_page))
        go_to_page = self.driver.find_element(By.XPATH, '//*[@id="button-1505"]')
        go_to_page.click()
        actual_page = int(input_page.get_attribute('value'))
        first_page = actual_page
        self.driver.implicitly_wait(10)

        # n = simpledialog.askinteger('ZOOM LEVEL', 'Enter the zoom level')

        # zoom = self.driver.find_element(By.XPATH, '//*[@id="button-1509"]')

        # for i in range(n):
        #     zoom.click()
        #     self.driver.implicitly_wait(10)


        page_html = self.driver.find_element(By.XPATH, '//*[@id="frmBookPDF_9168"]')
        # self.driver.switch_to.frame(page_html)
        # content = self.driver.find_element(By.XPATH, '//*[@id="pf1"]/div[1]')
        link = page_html.get_attribute('src')
        print(link)
        link_pattern = re.compile(r'&page=(\d+)&')
        link = re.sub(link_pattern, '&page=' + str(actual_page) + '&', link)
        self.driver.get(link)

        messagebox.showinfo('DISABLE JS', 'Please disable javascript and click OK')

        self.driver.execute_script('window.print();')
        self.driver.implicitly_wait(10)

        print('page ' + str(actual_page) + ' of ' + str(last_page))
        while actual_page < last_page:
            actual_page += 1

            self.driver.implicitly_wait(10)
            link = re.sub(link_pattern, '&page=' + str(actual_page) + '&', link)
            self.driver.get(link)
            self.driver.implicitly_wait(10)
            self.driver.execute_script('window.print();')
            self.driver.implicitly_wait(10)
            print('\rpage ' + str(actual_page) + ' of ' + str(last_page))

        folder_name = str(first_page) + '-' + str(actual_page)
        print('moving pdfs to pdf folder' + folder_name)
        os.makedirs('./pdf/' + folder_name, exist_ok=True)
        get_files = os.listdir('./pdf/')
        for file in get_files:
            if file.endswith('.pdf'):
                print('moving ' + file + ' to ' + folder_name)
                shutil.move('./pdf/' + file, './pdf/' + folder_name + '/', file)
        print('all pdfs moved to pdf folder ' + folder_name)



        # messagebox.showinfo('ADJUST ZOOM', 'Adjust the zoom level')
        # print('content: ' + content.text)
        # print(content.get_attribute('outerHTML'))

        # content.screenshot('./screenshots/page_' + str(actual_page) + '.png')
        # self.driver.switch_to.default_content()

        # while actual_page < last_page:
        #     next_page = self.driver.find_element(By.XPATH, '//*[@id="button-1521"]')
        #     next_page.click()
        #     actual_page = int(input_page.get_attribute('value'))
        #     self.driver.implicitly_wait(10)
        #     page_html = self.driver.find_element(By.XPATH, '//*[@id="frmBookPDF_9168"]')
        #     self.driver.switch_to.frame(page_html)
        #     content = self.driver.find_element(By.XPATH, '//*[@id="pf1"]/div[1]')

        #     content.screenshot('./ss/page_' + str(actual_page) + '.png')
        #     self.driver.switch_to.default_content()



if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes', report_name='reporte_prueba'))
    #unittest.main()
