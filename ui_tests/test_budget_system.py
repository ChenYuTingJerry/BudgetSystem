import os, unittest
from selenium import webdriver


class Selenium():
    def __init__(self):
        self.browser = webdriver.Chrome(
            executable_path=os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "..", "chromedriver.exe"))


class Budget(Selenium):
    def __init__(self):
        super(Budget, self).__init__()
        self.year = self.browser.find_element_by_name("year")
        self.month = self.browser.find_element_by_name("month")
        self.budget = self.browser.find_element_by_name("budget")
        self.create = self.browser.find_element_by_name("create")
        self.result = self.browser.find_element_by_tag_name('body')

    def create_budget(self, year, month, budget):
        self.budget.year.send_keys(year)
        self.budget.month.send_keys(month)
        self.budget.budget.send_keys(budget)
        self.budget.create.click()


class BudgetQuery(Selenium):
    def __init__(self):
        super(BudgetQuery, self).__init__()
        self.start = self.browser.find_element_by_name("start")
        self.end = self.browser.find_element_by_name("end")
        self.query = self.browser.find_element_by_name("query")
        self.result = self.browser.find_element_by_name("result").text


class TestBudgetSystem(unittest.TestCase):
    def setUp(self):
        self.budget = Budget()
        self.budget_query = BudgetQuery()
        self.addCleanup(self.budget.browser.quit)

    def tearDown(self):
        pass

    def test_create_budget(self):
        self.budget.browser.get("http://10.1.70.41:5000/budget")
        self.budget.create_budget("2020", "02", "10000")
        self.assertIn("SUCCESS!!", self.budget.result)

    def test_query_budget_1m_w_bgt(self):
        self.budget.delete_budget()
        self.budget.browser.get("http://10.1.70.41:5000/budget")
        self.budget.create_budget("2020", "01", "310")
        self.budget_query.browser.get("http://10.1.70.41:5000/budget/query")
        self.budget_query.query_budget("20200101", "20200131")
        self.assertEqual(310, self.budget_query.result)

    def test_query_budget_1d_w_bgt(self):
        self.budget.delete_budget()
        self.budget.browser.get("http://10.1.70.41:5000/budget")
        self.budget.create_budget("2020", "01", "310")
        self.budget_query.browser.get("http://10.1.70.41:5000/budget/query")
        self.budget_query.query_budget("20200101", "20200101")
        self.assertEqual(10, self.budget_query.result)

    def test_query_budget_10d_w_bgt(self):
        self.budget.delete_budget()
        self.budget.browser.get("http://10.1.70.41:5000/budget")
        self.budget.create_budget("2020", "01", "310")
        self.budget_query.browser.get("http://10.1.70.41:5000/budget/query")
        self.budget_query.query_budget("20200101", "20200110")
        self.assertEqual(100, self.budget_query.result)

    def test_query_budget_1m_wo_bgt(self):
        self.budget.delete_budget()
        self.budget_query.browser.get("http://10.1.70.41:5000/budget/query")
        self.budget_query.query_budget("20200201", "20200229")
        self.assertEqual(0, self.budget_query.result)



if __name__ == '__main__':
    unittest.main(verbosity=2)