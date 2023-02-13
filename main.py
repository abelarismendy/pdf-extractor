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
import merge
import compress


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
options.add_argument('--kiosk-printing')
# options.add_argument("--window-size=2000,2000")


# options.add_experimental_option('detach', True)

script_route = os.path.realpath(__file__)
script_folder = os.path.dirname(script_route)
print(script_folder)

def rename_files(first_page, actual_page, book_id):

    folder_name = str(first_page) + '-' + str(actual_page)
    print('moving pdfs to pdf folder ' + folder_name)
    os.makedirs(f'./pdf/{book_id}/' + folder_name, exist_ok=True)
    get_files = os.listdir(f'./pdf/{book_id}/')
    for file in get_files:
        if file.endswith('.pdf'):
            print('moving ' + file + ' to ' + folder_name)
            shutil.move(f'./pdf/{book_id}/' + file, f'./pdf/{book_id}/' + folder_name + '/', file)
    print('all pdfs moved to pdf folder ' + folder_name)



class LoginUniandes(unittest.TestCase):
    def setUp(self):
        self.book_id = simpledialog.askstring('BOOK ID', 'Enter the book id (4 digits)')
        os.makedirs(f'./pdf/{self.book_id}/', exist_ok=True)
        prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings), 'savefile.default_directory': f'{script_folder}/pdf/{self.book_id}/'}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(executable_path= chrome_path,options=options)
        self.driver.get('https://login.ezproxy.uniandes.edu.co/login?qurl=http://www.ebooks7-24.com%2f%3fil%3d' + self.book_id)
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
            last_page = 1000

        # select pages range

        self.assertGreater(last_page, first_page)
        self.assertGreater(last_page, 0)
        self.assertLessEqual(last_page, 2000)


        input_page = self.driver.find_element(By.XPATH, f'//*[@id="VIEWER_page{self.book_id}-inputEl"]')
        input_page.clear()
        input_page.send_keys(str(first_page))
        go_to_page = self.driver.find_element(By.XPATH, '//*[@id="button-1505"]')
        go_to_page.click()
        actual_page = int(input_page.get_attribute('value'))
        first_page = actual_page
        self.driver.implicitly_wait(10)

        page_html = self.driver.find_element(By.XPATH, f'//*[@id="frmBookPDF_{self.book_id}"]')

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
            print('\r')
            print('\rpage ' + str(actual_page) + ' of ' + str(last_page))
            if actual_page - first_page == 100:
                rename_files(first_page, actual_page, self.book_id)
                first_page = actual_page + 1
        rename_files(first_page, actual_page, self.book_id)
        # merge pdfs
        merge.merge_book(self.book_id)

        # compress pdf
        book_path = f'./books/{self.book_id}.pdf'
        book_output_path = f'./books/{self.book_id}_compressed.pdf'
        compress.compress(book_path, book_output_path, power=3)


if __name__ == '__main__':
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes', report_name='reporte_prueba'))
    # rename_files(502, 529, '9346')
    # merge.merge_book('9346')
