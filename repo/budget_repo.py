import sqlite3


class BudgetRepo:
    def get_all(self, start, end):
        with sqlite3.connect("budget.db") as con:
            c = con.cursor()
            rows = c.execute(f"SELECT * FROM budget "
                             f"where (year between {start['year']} and {end['year']}) "
                             f"and (month between {start['month']} and {end['month']})")
            for row in rows:
                print(row)

    def delete_all(self):
        with sqlite3.connect("budget.db") as con:
            c = con.cursor()
            c.execute(f"DELETE FROM budget")
            con.commit()

    def insert_data(con, year, month, budget):
        c = con.cursor()
        c.execute(f"INSERT INTO budget VALUES ({year},{month}, {budget})")
        con.commit()

    def update_data(con, year, month, budget):
        c = con.cursor()
        c.execute(f"UPDATE budget SET BUDGET = '{budget}' WHERE year = '{year}' and month='{month}'")
        con.commit()


if __name__ == "__main__":
    repo = BudgetRepo()
    repo.delete_all()