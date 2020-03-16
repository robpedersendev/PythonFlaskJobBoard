from flask import Flask, g, render_template
import sqlite3

PATH = 'db/jobs.sqlite'

app = Flask(__name__, template_folder="templates")  # __name__ is the name of the current


# Python module. The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell
# it that.
# static_folder: Specifies the name of the folder where static assets will be served.
# template_folder: Specifies the name of the folder where templates will be served.


def open_connection():
    connection = getattr(g, "_connection", None)
    if connection is None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection


def execute_sql(sql: object, values: object = (), commit: object = False, single: object = False) -> object:
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit is True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()
    cursor.close()
    return results


@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, "_connection", None)
    print(connection)
    if connection is not None:
        connection.close()


@app.route('/job/<job_id>')
def job(job_id):
    job = execute_sql(
        'SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)


@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql(
        'SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)
