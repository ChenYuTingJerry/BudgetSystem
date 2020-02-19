import os, unittest
from selenium import webdriver


class TestBudgetSystem(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chromedriver.exe"))
        self.addCleanup(self.browser.quit)

    def tearDown(self):
        pass

    def test_create_budget(self):
        self.browser.get("http://10.1.70.41:5000/budget")
        year = self.browser.find_element_by_name("year")
        year.send_keys("2020")
        month = self.browser.find_element_by_name("month")
        month.send_keys("02")
        budget = self.browser.find_element_by_name("budget")
        budget.send_keys("10000")
        create = self.browser.find_element_by_name("create")
        create.click()
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn("SUCCESS!!", text)


if __name__ == '__main__':
    unittest.main(verbosity=2)