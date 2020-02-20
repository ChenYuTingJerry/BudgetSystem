from calendar import monthrange
from datetime import datetime

from repo.budget_repo import BudgetRepo


class BudgetManager:
    def __init__(self):
        self._repo = BudgetRepo()

    def calculate_amount_by_start_end_date(self, start_date, end_date):
        start_date_query = self._extract_year_and_month(start_date)
        end_date_query = self._extract_year_and_month(end_date)
        result_from_query = self._repo.get_all(start_date_query, end_date_query)
        req_query = self._filter(start_date_query, end_date_query, result_from_query)
        print(req_query)

        m = {
            start_date['month']: start_date['day'],
            end_date['month']: end_date['day'],
        }
        if req_query:
            for row in req_query:
                day = m.get(row[1])
                if day:
                    pass
            amount = sum(int([row[2]/(row[1]/row[3]) for row in req_query])
            return amount
        return 0

    def _filter(self, start_date_query, end_date_query, result_from_query):
        result = list()
        for row in result_from_query:
            if start_date_query['year'] <= row[0] <= end_date_query['year'] and \
                    start_date_query['month'] <= row[1] <= end_date_query['month']:
                row_in = list(row)
                row_in.append(monthrange(row[0], row[1])[1])
                result.append(tuple(row_in))
        return result

    @staticmethod
    def _extract_year_and_month(_date: datetime):
        year = _date.year
        month = _date.month
        return {
            "year": _date.year,
            "month": _date.month,
            "day": _date.day,
            "total_days": monthrange(year, month)[1]
        }

