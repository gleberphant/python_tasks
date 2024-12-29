"""
    TODO - Notificar o lembrete pelo ZAP
    TODO - ADICIONAR GRUPO de notificações
    TODO - adicionar pessoa responsável
    TODO - adicionar controle usuário
    TODO - converter em SPA com objetos JSON
"""

import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)


@app.route("/<int:task_id>", methods=['POST'])
def delete_or_update_task(task_id):
    """ Deleta ou atualiza uma tarefa da lista """

    match request.form.get("_method"):
        case "DELETE":
            task_parameters  = (task_id, )
            sql_query = "DELETE FROM tasks WHERE id=?"

        case "PUT":
            if request.args.get("complete"):
                task_parameters = ("true" if request.args.get("complete") == "false" else "false", task_id )
                sql_query = "UPDATE tasks SET concluded=? WHERE id=?"
            else:
                flash("Método inválido!")
                return redirect(url_for("list_tasks"))
        case _:
            flash("Método inválido!")
            return redirect(url_for("list_tasks"))

    if sql_query and task_parameters:
        with sqlite3.connect("database.db") as con:
            try:
                con.execute(sql_query, task_parameters)
                return redirect(url_for("list_tasks"))

            except Exception as e:
                flash(f"ERRO ({e})")
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


#
# @app.route("/delete/<int:task_id>", methods=['POST', 'DELETE'])
# def delete_task(task_id):
#     """ Deleta uma tarefa da lista """
#
#     if request.form.get("_method") == "DELETE":
#         with sqlite3.connect("database.db") as con:
#
#             task_parameters  = (task_id, )
#             try:
#                 con.execute("DELETE FROM tasks WHERE id=?",task_parameters )
#             except Exception as e:
#                 return f"Erro ao deletar ({e})"
#
#     return redirect(url_for("list_tasks"))
#
#
# @app.route("/complete/<int:task_id>", methods=['POST'])
# def check_task(task_id):
#     """  Marca uma tarefa como concluída ou não"""
#
#     if request.form.get("_method") == "PUT":
#         with sqlite3.connect("database.db") as con:
#
#             task_parameters = ("true" if request.args.get("complete")== "false" else "false", task_id )
#             try:
#                 con.execute("UPDATE tasks SET concluded=? WHERE id=? ", task_parameters )
#             except Exception as e:
#                 return f"Erro ao concluir ({e})"
#
#     return redirect(url_for("list_tasks"))

if __name__ =="__main__":

    app.run(debug=True)
