from flask import Flask, render_template
import PySQLite

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    result = []
    r = PySQLite.unassignedCases
    for x in r:
        result.append(x`)
        return render_template("test_index.html", result=result)

@app.route("/query")
def query():
    return render_template("test_query.html")\

@app.route("/entry")
def entry():
    return render_template("test_entry.html")

if __name__ == "__main__":
    app.run(debug=True)








































