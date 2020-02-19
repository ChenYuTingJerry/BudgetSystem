import unittest
import run
from mock import MagicMock
from testfixtures import Replacer


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

        result = self.app.post("/budget", data=dict(
            year="2020",
            month="2",
            budget="10000"
        ))

        expeced = b'\n    <form method="POST" action="/budget">\n        Year <input type="text" name="year">\n        Month <input type="text" name="month">\n        Budget <input type="text" name="budget">\n        <input name="create" type="submit" value="Create">\n    </form>\n    SUCCESIS!!!\n    '

        self.assertEquals(result.status, "200 OK")
        self.assertEquals(result.data, expeced)

        #mock_insert_data.assert_called()

    def test_update_budget(self):
        mock_check_data_exist = MagicMock()
        mock_check_data_exist.return_value = True
        self.replacer.replace("run.check_data_exist", mock_check_data_exist)

        mock_update_data = MagicMock()
        self.replacer.replace("run.insert_data", mock_update_data)

        result = self.app.post("/budget", data=dict(
            year="2020",
            month="2",
            budget="10000"
        ))

        expeced = b'\n    <form method="POST" action="/budget">\n        Year <input type="text" name="year">\n        Month <input type="text" name="month">\n        Budget <input type="text" name="budget">\n        <input name="create" type="submit" value="Create">\n    </form>\n    SUCCESIS!!!\n    '

        self.assertEquals(result.status, "200 OK")
        self.assertEquals(result.data, expeced)

        #mock_update_data.assert_called()


if __name__ == '__main__':
    unittest.main()
