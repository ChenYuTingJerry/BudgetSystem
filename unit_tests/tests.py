import unittest
from datetime import datetime, date

import run
from mock import MagicMock
from testfixtures import Replacer

from model.budget_manager import BudgetManager
from repo.budget_repo import BudgetRepo


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = run.app.test_client()
        self.replacer = Replacer()
        self.replacer.replace("sqlite3.connect", MagicMock())

    def tearDown(self):
        self.replacer.restore()

    def test_create_budget(self):
        mock_check_data_exist = MagicMock()
        mock_check_data_exist.return_value = False
        self.replacer.replace("run.check_data_exist", mock_check_data_exist)

        mock_insert_data = MagicMock()
        self.replacer.replace("run.insert_data", mock_insert_data)
        mock_update_data = MagicMock()
        self.replacer.replace("run.update_data", mock_update_data)

        result = self.app.post("/budget", data=dict(
            year="2020",
            month="2",
            budget="10000"
        ))

        expeced = b'\n    <form method="POST" action="/budget">\n        Year <input type="text" name="year">\n        Month <input type="text" name="month">\n        Budget <input type="text" name="budget">\n        <input name="create" type="submit" value="Create">\n    </form>\n    SUCCESIS!!!\n    '

        self.assertEqual(result.status, "200 OK")
        self.assertEqual(result.data, expeced)

        mock_insert_data.assert_called()

    def test_update_budget(self):
        mock_check_data_exist = MagicMock()
        mock_check_data_exist.return_value = True
        self.replacer.replace("run.check_data_exist", mock_check_data_exist)

        mock_insert_data = MagicMock()
        self.replacer.replace("run.insert_data", mock_insert_data)
        mock_update_data = MagicMock()
        self.replacer.replace("run.update_data", mock_update_data)

        result = self.app.post("/budget", data=dict(
            year="2020",
            month="2",
            budget="10000"
        ))

        expeced = b'\n    <form method="POST" action="/budget">\n        Year <input type="text" name="year">\n        Month <input type="text" name="month">\n        Budget <input type="text" name="budget">\n        <input name="create" type="submit" value="Create">\n    </form>\n    SUCCESIS!!!\n    '

        self.assertEqual(result.status, "200 OK")
        self.assertEqual(result.data, expeced)

        mock_update_data.assert_called()


class BudgetManagerTestCase(TestCase):
    def test_query_budget_with_full_month(self):
        expected = 310
        mock_get_all = MagicMock()
        mock_get_all.return_value = [(2020, 1, 310), (2020, 2, 31)]
        self.replacer.replace("repo.budget_repo.BudgetRepo.get_all", mock_get_all)
        manager = BudgetManager()
        start_date = date.fromisoformat('2020-01-01')
        end_date = date.fromisoformat('2020-01-31')
        result = manager.calculate_amount_by_start_end_date(start_date, end_date)

        self.assertEqual(result, expected)

    def test_query_budget_with_two_month(self):
        expected = 341
        mock_get_all = MagicMock()
        mock_get_all.return_value = [(2020, 1, 310), (2020, 2, 31)]
        self.replacer.replace("repo.budget_repo.BudgetRepo.get_all", mock_get_all)
        manager = BudgetManager()
        start_date = date.fromisoformat('2020-01-01')
        end_date = date.fromisoformat('2020-02-29')
        result = manager.calculate_amount_by_start_end_date(start_date, end_date)

        self.assertEqual(result, expected)

    def test_query_budget_with_days(self):
        expected = 10
        mock_get_all = MagicMock()
        mock_get_all.return_value = [(2020, 1, 310), (2020, 2, 31)]
        self.replacer.replace("repo.budget_repo.BudgetRepo.get_all", mock_get_all)
        manager = BudgetManager()
        start_date = date.fromisoformat('2020-01-01')
        end_date = date.fromisoformat('2020-01-01')
        result = manager.calculate_amount_by_start_end_date(start_date, end_date)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
