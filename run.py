from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import datetime
from model.budget_manager import BudgetManager

app = Flask(__name__)


@app.route('/budget', methods=['GET'])
def show_budget():
    return '''
    <form method="POST" action="/budget">
        Year <input type="text" name="year">
        Month <input type="text" name="month">
        Budget <input type="text" name="budget">
        <input name="create" type="submit" value="Create">
    </form>
    '''


@app.route('/budget', methods=['POST'])
def create_budget():
    year = request.form['year']
    month = request.form['month']
    budget = request.form['budget']
    with sqlite3.connect("budget.db") as con:
        if check_data_exist(con, year, month):
            update_data(con, year, month, budget)
        else:
            insert_data(con, year, month, budget)

    return '''
    <form method="POST" action="/budget">
        Year <input type="text" name="year">
        Month <input type="text" name="month">
        Budget <input type="text" name="budget">
        <input name="create" type="submit" value="Create">
    </form>
    SUCCESIS!!!
    '''


@app.route("/query.html")
def index():
    return render_template("query.html")


@app.route('/budget/query', methods=['POST'])
def query_budget():
    start = request.form['start']
    end = request.form['end']
    start_date = datetime.strptime(start, "%Y%m%d")
    end_date = datetime.strptime(end, "%Y%m%d")

    budget_manager = BudgetManager()
    totol_amount = budget_manager.calculate_amount_by_start_end_date(start_date, end_date)
    result = "%.2f" % round(totol_amount, 2)
    return result


def check_data_exist(con, year, month):
    c = con.cursor()
    c.execute(f"select count(*) from budget  where year = '{year}' and month='{month}'")
    count = c.fetchone()[0]
    if count == 0:
        return False
    else:
        return True


def insert_data(con, year, month, budget):
    c = con.cursor()
    c.execute(f"INSERT INTO budget VALUES ({year},{month}, {budget})")
    con.commit()


def update_data(con, year, month, budget):
    c = con.cursor()
    c.execute(f"UPDATE budget SET BUDGET = '{budget}' WHERE year = '{year}' and month='{month}'")
    con.commit()


if __name__ == '__main__':
    app.run(host='10.1.70.41', debug=True)
