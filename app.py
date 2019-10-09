from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    result = ['19001234', '20191001', 'Test case']
    return render_template("index.html", result=result)

@app.route("/entry")
def entry():
    return render_template("entry.html")

@app.route("/query")
def query():
    return render_template("query.html")

if __name__ == "__main__":
    app.run(debug=True)
