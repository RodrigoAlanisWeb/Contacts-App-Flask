from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'

mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()

    return render_template('index.html', contacts=data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES(%s, %s, %s)',
                    (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added succesfully')

        return redirect(url_for('index'))


@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM contacts WHERE id = {id}')
    data = cur.fetchall()
    return render_template('edit.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur.execute(f"UPDATE contacts SET fullname = '{fullname}',email = '{email}',phone = '{phone}' WHERE id = {id}")
        mysql.connection.commit()
        flash('Contact Updated Successfully')

        return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM contacts WHERE id = {id}')
    mysql.connection.commit()
    flash('Contact Deleted Successfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
