import unittest
import run
from mock import MagicMock
from testfixtures import Replacer

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = run.app.test_client()
        self.replacer = Replacer()

    def tearDown(self):
        self.replacer.restore()

    def test_create_budget(self):
        mock_db = self.replacer.replace("sqlite3.connect", MagicMock())
        result = self.app.post("/budget", data=dict(
            year="2020",
            month="2",
            budget="10000"
        ))

        expeced = b'\n    <form method="POST" action="/budget">\n        Year <input type="text" name="year">\n        Month <input type="text" name="month">\n        Budget <input type="text" name="budget">\n        <input name="create" type="submit" value="Create">\n    </form>\n    SUCCESS!!\n    '
        print(expeced)
        print(result.data)
        self.assertEquals(result.status, "200 OK")
        self.assertEquals(result.data, expeced)


if __name__ == '__main__':
    unittest.main()
