from flask import Flask, render_template, request

from metric import start_test
from collect_docs import collect
from Search import search

app = Flask("App")


@app.route("/")
def main_page():
    return render_template("main.html")


def test(txt):
    return txt


@app.route("/logical_search", methods=["POST", "GET"])
def logical_search():
    if request.method == "POST":
        if request.form["query"]:
            result = search(request.form["query"])
            if len(result) == 0:
                flag = "There is no documents according to your query or natural language question, sorry!"
                return render_template("logical_search.html", flag=flag)
            else:
                flag = "We have some documents for you, that correspond your query or natural language question!"
                return render_template("logical_search.html", result=result, flag=flag, test=test)
    else:
        return render_template("logical_search.html")


@app.route("/update_base", methods=["POST", "GET"])
def update_base():
    if request.method == "POST":
        current_files = collect(request.form["url"], request.form["name"])
        return render_template("update_base.html", result=current_files)
    else:
        return render_template("update_base.html")


@app.route("/info_about_metrix", methods=["POST", "GET"])
def info_about_metrix():
    if request.method == "POST":
        result = start_test()
        return render_template("info_about_metrix.html", result=result)
    else:
        return render_template("info_about_metrix.html")


@app.route("/help")
def help():
    return render_template("help.html")


if __name__ == '__main__':
    app.run(debug=True)
