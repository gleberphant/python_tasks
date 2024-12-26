import sqlite3

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route("/delete", methods=['POST'])
def delete():
    with sqlite3.connect("database.db") as con:
        if request.form.get("id"):
            del_id = request.form.get("id")
            try:
                con.execute("DELETE FROM tasks WHERE id=?",(del_id, ) )
            except Exception as e:
                return f"Erro ao deletar {e}"

    return redirect(url_for("index_get"))


@app.route("/", methods=['POST'])
def index_post():
    # se method post tenta inserir nova task

    with  sqlite3.connect("database.db") as con:
        #configura para os resultados das query retornar objetos ROW/DICT
        con.row_factory = sqlite3.Row

        if request.form.get("task"):
            new_task = request.form.get("task")
            try:
                con.execute("INSERT INTO tasks (task) values (?)", (new_task, ))
            except Exception as e:
                return f"erro ao inserir nova task {e}"

    return redirect( url_for("index_get"))


@app.route("/", methods=['GET'])
def index_get():


    with sqlite3.connect("database.db") as con:
        con.row_factory = sqlite3.Row
        result = con.execute("SELECT * FROM tasks").fetchall()


    return render_template("index.html", result=result)

if __name__ =="__main__":
    app.run(debug=True)