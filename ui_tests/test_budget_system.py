import os, unittest
from selenium import webdriver


class TestBudgetSystem(unittest.TestCase):
    def setUp(self):
        self._year, self._month, self._budget, self._create = None, None, None, None
        self.browser = webdriver.Chrome(
            executable_path=os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "..", "chromedriver.exe"))
        self.addCleanup(self.browser.quit)

    def tearDown(self):
        pass

    @property
    def year(self):
        if not self._year:
            self._year = self.browser.find_element_by_name("year")
        return self._year

    @property
    def month(self):
        if not self._month:
            self._month = self.browser.find_element_by_name("month")
        return self._month

    @property
    def budget(self):
        if not self._budget:
            self._budget = self.browser.find_element_by_name("budget")
        return self._budget

    @property
    def create(self):
        if not self._create:
            self._create = self.browser.find_element_by_name("create")
        return self._create

    def test_create_budget(self):
        self.browser.get("http://10.1.70.41:5000/budget")
        self.year.send_keys("2020")
        self.month.send_keys("02")
        self.budget.send_keys("10000")
        self.create.click()
        self.assertIn("SUCCESS!!", self.browser.find_element_by_tag_name('body').text)


if __name__ == '__main__':
    unittest.main(verbosity=2)