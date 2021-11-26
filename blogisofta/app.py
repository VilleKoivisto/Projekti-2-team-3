# postgres-toiminnallisuus
import psycopg2
from query_config import config

# flask-kirjastot ym.
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


# Muodostetaan tietokannan yhteysobjekti
# -------------------------------------------------------------------------------------
def get_db_connection():
    con = psycopg2.connect(**config())
    cursor = con.cursor()
    
    # cursor-muuttujaan viitataan nimellä conn funktion ulkopuolella, TODO: muuta
    return cursor


# Haetaan blogi-postauksen vastaava rivi tietokannasta
# -------------------------------------------------------------------------------------
def get_post(post_id):
    cursor = get_db_connection()

    SQL = f"SELECT * FROM posts WHERE id = %s;"

    cursor.execute(SQL, (post_id,))
    post = cursor.fetchone()
    
    cursor.close()

    if post is None:
        abort(404)
    
    return post


# Luodaan flask-objekti
# -------------------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'do_not_touch_or_you_will_be_fired'


# Muotoillaan tietokannan datetime-objekti luettavampaan muotoon
# esim.: 2021-07-20 10:36:36 -> 20.07.2021 klo 10:36
# -------------------------------------------------------------------------------------
def format_date(post_date):
    
    return post_date.strftime('%d.%m.%Y') + ' klo ' + post_date.strftime('%H:%M')


# Tulostetaan kaikki blogimerkintöjen otsikot ym. aloitussivulle
# -------------------------------------------------------------------------------------
@app.route('/')
def index():

    cursor = get_db_connection()

    SQL = f"SELECT * FROM posts;"
        
    cursor.execute(SQL)
    posts = cursor.fetchall()

    cursor.close()

    # haetaan kaikki rivit tietokannasta listaan
    dictrows = []

    for row in posts:
        row_dict = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}
        dictrows.append(row_dict)
    
    # muotoillaan päivämäärät
    for post in dictrows:
        post['created'] = format_date(post['created'])
    
    return render_template('index.html', posts=dictrows)
    

# Haetaan blogi-postaus tietokannasta ja näytetään se selaimessa
# -------------------------------------------------------------------------------------
@app.route('/<int:post_id>')
def post(post_id):
    
    row = get_post(post_id)
    post = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}

    post['created'] = format_date(post['created'])
    return render_template('post.html', post=post)


# Luodaan uusi merkintä blogiin
# -------------------------------------------------------------------------------------
@app.route('/create', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        else:
            con = psycopg2.connect(**config())
            cursor = con.cursor()

            SQL = f"INSERT INTO posts (title, content) VALUES (%s,%s);"
            insert_values = (title, content)
            
            cursor.execute(SQL, insert_values)
            con.commit()

            cursor.close()
            return redirect(url_for('index'))

    return render_template('create.html')


# Muokataan blogi-postausta
# -------------------------------------------------------------------------------------
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):

    row = get_post(id)
    post = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        else:
            con = psycopg2.connect(**config())
            cursor = con.cursor()

            SQL = f"UPDATE posts SET title = %s, content = %s WHERE id = %s"
            insert_values = (title, content, id)
            
            cursor.execute(SQL, insert_values)

            con.commit()
            cursor.close()

            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


# Poistetaan yksittäinen blogi-postaus
# -------------------------------------------------------------------------------------
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):

    row = get_post(id)
    post = {"id": row[0], "created": row[1], "title": row[2], "content": row[3]}

    con = psycopg2.connect(**config())
    cursor = con.cursor()
    
    SQL = f"DELETE FROM posts WHERE id = %s"
    insert_values = (id,)
    
    cursor.execute(SQL, insert_values)
    
    con.commit()
    cursor.close()

    flash('"{}" was successfully deleted!'.format(post['title']))
    
    return redirect(url_for('index'))
