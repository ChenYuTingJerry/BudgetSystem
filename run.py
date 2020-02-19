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
        <input type="submit" value="Create">
    </form>
    '''


@app.route('/budget', methods=['POST'])
def create_budget():
    year = request.form['year']
    month = request.form['month']
    budget = request.form['budget']
    with sqlite3.connect("budget.db") as con:
        c = con.cursor()
        c.execute(f"INSERT INTO budget VALUES ({year},{month}, {budget})")
        con.commit()
    return '''SUCCESS'''


if __name__ == '__main__':
    app.run(debug=True)
