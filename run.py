from flask import Flask, jsonify, request
import sqlite3

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
            insert_data(con, year, month, budget)
        else:
            update_data(con, year, month, budget)

    return '''
    <form method="POST" action="/budget">
        Year <input type="text" name="year">
        Month <input type="text" name="month">
        Budget <input type="text" name="budget">
        <input name="create" type="submit" value="Create">
    </form>
    SUCCESS!!
    '''


def check_data_exist(con, year, month):
    c = con.cursor()
    c.execute(f"select count(*) from budget  where year = '{year}' and month='{month}'")
    count = c.fetchone()[0]
    if count == 0:
        return True
    else:
        return False


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
