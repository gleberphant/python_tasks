"""
    TODO - Notificar o lembrete pelo ZAP
    TODO - ADICIONAR GRUPO de notificações
    TODO - adicionar pessoa responsável
    TODO - adicionar controle usuário
"""


import sqlite3
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route("/delete", methods=['POST'])
def delete_task():
    """ Deleta uma tarefa da lista """

    with sqlite3.connect("database.db") as con:
        if request.form.get("id"):
            task_parameters  = (request.form.get("id"), )
            try:
                con.execute("DELETE FROM tasks WHERE id=?",task_parameters )
            except Exception as e:
                return f"Erro ao deletar ({e})"

    return redirect(url_for("list_tasks"))




@app.route("/<int:task_id>/<task_complete>", methods=['GET'])
def check_task(task_id, task_complete):
    """  Marca uma tarefa como concluída ou não"""

    with sqlite3.connect("database.db") as con:
        if task_id:

            task_parameters = ("true" if task_complete == "false" else "false", task_id )

            try:
                con.execute("UPDATE tasks SET concluded=? WHERE id=? ", task_parameters )
            except Exception as e:
                return f"Erro ao concluir ({e})"

    return redirect(url_for("list_tasks"))



@app.route("/", methods=['POST'])
def add_task():
    """ Cria uma nova tarefa """

    with  sqlite3.connect("database.db") as con:
        #configura para os resultados das query retornar objetos ROW/DICT
        con.row_factory = sqlite3.Row

        if request.form.get("task"):
            deadline = request.form.get("deadline") if request.form.get("deadline") else "*-*-*"

            task_parameters  = ( request.form.get("task"), deadline)
            try:
                con.execute("INSERT INTO tasks (task, deadline, concluded) values (?, ?, 'false')", task_parameters )
            except Exception as e:
                return f"erro ao inserir nova task ({e})"

    return redirect( url_for("list_tasks"))



@app.route("/", methods=['GET'])
def list_tasks():
    """ Mostra lista de tarefas"""

    with sqlite3.connect("database.db") as con:
        con.row_factory = sqlite3.Row
        result = con.execute("SELECT * FROM tasks").fetchall()


    return render_template("list_tasks.html", result=result)


if __name__ =="__main__":
    app.run(debug=True)