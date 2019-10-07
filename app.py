from flask import Flask, render_template
import PySQLite

app = Flask(__name__)

@app.route("/")
def index():
    result = ['19001234', '20191001', 'Test case']
    headline = "Eagan Police Department"
    return render_template("index.html", headline=headline, result=result)
    # r = PySQLite.unassignedCases
    #     for x in r:
    #         result.append(x)
    #     return render_template("test_index.html", result=result)

@app.route("/entry")
def entry():
    return render_template("entry.html")

@app.route("/query")
def query():
    return render_template("query.html")

if __name__ == "__main__":
    app.run(debug=True)








































