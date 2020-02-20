from datetime import datetime

from repo.budget_repo import BudgetRepo


class BudgetManager:
    def __init__(self):
        self._repo = BudgetRepo()

    def calculate_amount_by_start_end_date(self, start_date, end_date):
        start_date_query = self._extract_year_and_month(start_date)
        end_date_query = self._extract_year_and_month(end_date)
        result_from_query = self._repo.get_all(start_date_query, end_date_query)
        amount = sum([row[2] for row in result_from_query])
        return amount

    @staticmethod
    def _extract_year_and_month(_date: datetime):
        return {
            "year": _date.year,
            "month": _date.month
        }
